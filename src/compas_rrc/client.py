import threading
import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Union

import roslibpy
from compas_eve import Message
from compas_eve import Publisher
from compas_eve import Subscriber
from compas_eve import Topic
from compas_eve import Transport
from compas_eve.ros import RosTransport

from .common import CLIENT_PROTOCOL_VERSION
from .common import FutureResult
from .common import InstructionException
from .message import Instruction
from .message import RobotMessage

__all__ = ["RosClient", "AbbClient"]


FEEDBACK_ERROR_PREFIX = "Done FError "

PROTOCOL_VERSION_TOPIC = "protocol_version"
"""Topic on which the driver announces its protocol version, relative to the namespace."""

PROTOCOL_VERSION_TIMEOUT = 10
"""Seconds to wait for the driver to announce its protocol version."""

FeedbackMessage = Union[RobotMessage, Dict[str, Any]]
"""A message received from the driver.

ROS delivers raw dictionaries while other transports decode into a
:class:`RobotMessage`; both are read the same way, with ``message["key"]``.
"""

Connection = Union[Transport, roslibpy.Ros]
"""Anything :class:`AbbClient` can talk over."""


class RosClient(RosTransport):
    """Connection to a ROS bridge, for use with :class:`AbbClient`.

    This is a ``compas_eve`` ROS transport that also exposes the handful of
    ``roslibpy.Ros`` methods RRC scripts have always called, so existing code
    keeps working unchanged.

    Parameters
    ----------
    host : :obj:`str`
        Host name of the ROS bridge. Defaults to ``localhost``.
    port : :obj:`int`
        Port of the ROS bridge. Defaults to ``9090``.
    connect_timeout : :obj:`float`
        Seconds to wait for the connection to be established.

    Examples
    --------
    ::

        ros = rrc.RosClient()
        ros.run()

        abb = rrc.AbbClient(ros, '/rob1')

        ros.close()

    Notes
    -----
    The connection is established when the client is constructed rather than
    when :meth:`run` is called, because that is how ``compas_eve`` transports
    work. :meth:`run` is kept as a no-op so that existing scripts, which call
    it right after constructing the client, keep working.
    """

    def run(self, timeout: Optional[float] = None) -> None:
        """Kept for backwards compatibility. The connection is already established."""

    def terminate(self) -> None:
        """Terminate the connection. :meth:`close` already does this."""
        if self.client.is_connected:
            self.client.terminate()

    def on_ready(self, callback: Callable[[], None]) -> None:
        """Invoke a callback when the connection is ready."""
        self.client.on_ready(callback)

    def get_params(self) -> List[str]:
        """Retrieve the list of parameters on the ROS parameter server."""
        return self.client.get_params()

    @property
    def is_connected(self) -> bool:
        """:obj:`bool`: Indicates whether the connection is open."""
        return self.client.is_connected


class _AttachedRosTransport(RosTransport):
    """A :class:`compas_eve.ros.RosTransport` bound to a connection someone else owns.

    ``RosTransport`` always creates and connects its own ``roslibpy.Ros``, which
    is what :class:`RosClient` wants. This variant reuses a connection that
    already exists, so a script holding a ``roslibpy.Ros`` -- including anything
    deriving from it -- can hand it to :class:`AbbClient` the way it used to.

    The attributes below mirror ``RosTransport.__init__`` minus the connect
    step; keep them in sync when upgrading ``compas_eve``.
    """

    def __init__(self, client: roslibpy.Ros) -> None:
        Transport.__init__(self)
        self.host = getattr(client, "host", None)
        self.port = getattr(client, "port", None)
        self.client = client
        self._publishers: Dict[str, roslibpy.Topic] = {}
        self._subscribers: Dict[str, roslibpy.Topic] = {}
        self._topic_configs: Dict[str, Any] = {}
        self._subscriptions: Dict[str, Dict[str, Callable]] = {}
        self._subscription_handlers: Dict[str, Callable] = {}
        self._local_callbacks: Dict[str, Any] = {}
        self._advertised_topics: Set[str] = set()


def _as_transport(client: Connection) -> Transport:
    """Return a ``compas_eve`` transport for whatever the caller passed in."""
    if isinstance(client, Transport):
        return client

    if isinstance(client, roslibpy.Ros):
        return _AttachedRosTransport(client)

    raise TypeError("Expected a compas_eve transport or a roslibpy client, got: {!r}".format(client))


def _robot_message_topic(transport: Transport, name: str, **ros_options: Any) -> Topic:
    """Build the topic carrying RRC robot messages.

    ROS moves the payload in the driver's own message type and needs its name
    plus the queue settings the driver expects. Every other transport carries
    the payload itself and decodes it into a :class:`RobotMessage`.
    """
    if isinstance(transport, RosTransport):
        return Topic(name, RobotMessage.ROS_MSG_TYPE, **ros_options)

    return Topic(name, RobotMessage)


def _protocol_version_topic(transport: Transport, name: str) -> Topic:
    """Build the topic on which the driver announces its protocol version."""
    if isinstance(transport, RosTransport):
        return Topic(name, "std_msgs/String", queue_size=1)

    return Topic(name, Message)


def _get_key(message: RobotMessage) -> str:
    return "msg:{}".format(message.sequence_id)


def _get_response_key(message: FeedbackMessage) -> str:
    return "msg:{}".format(message["feedback_id"])


class SequenceCounter:
    """An atomic, thread-safe sequence increament counter."""

    ROLLOVER_THRESHOLD = 1000000

    def __init__(self, start: int = 0) -> None:
        """Initialize a new counter to given initial value."""
        self._lock = threading.Lock()
        self._value = start

    def increment(self, num: int = 1) -> int:
        """Atomically increment the counter by ``num`` and
        return the new value.
        """
        with self._lock:
            self._value += num
            if self._value > SequenceCounter.ROLLOVER_THRESHOLD:
                self._value = 1
            return self._value

    @property
    def value(self) -> int:
        """Current sequence counter."""
        with self._lock:
            return self._value


def default_feedback_parser(result: FeedbackMessage) -> Union[str, InstructionException]:
    feedback_value = result["feedback"]

    if feedback_value.startswith(FEEDBACK_ERROR_PREFIX):
        return InstructionException(feedback_value, result)

    return feedback_value


class AbbClient:
    """Client used to communicate with ABB robots via ROS.

    This client handles all communication over ROS topics, and implements
    blocking behaviors as an application-level construct.

    Examples
    --------

    Connection example to a single robot::

        # Create Ros Client
        ros = rrc.RosClient()
        ros.run()

        # Create ABB Client
        abb = rrc.AbbClient(ros, '/rob1')
        print('Connected.')

        # Close client
        ros.close()
        ros.terminate()

    Advance connection example to multiple robots::

        # Create Ros Client
        ros = rrc.RosClient()
        ros.run()

        # Create ABB Clients
        abb_rob1 = rrc.AbbClient(ros, '/rob1')
        abb_rob2 = rrc.AbbClient(ros, '/rob2')

        # Clients are connected
        print('Connected.')

        # Print Text
        abb_rob1.send(rrc.PrintText('Hello Robot 1'))
        abb_rob2.send(rrc.PrintText('Hello Robot 2'))

        # Close client
        ros.close()
        ros.terminate()

    """

    def __init__(self, transport: Connection, namespace: str = "/rob1") -> None:
        """Initialize a new robot client instance.

        Parameters
        ----------
        transport : :class:`compas_eve.Transport` or :class:`roslibpy.Ros`
            Connection over which to talk to the driver. Use :class:`RosClient`
            for ROS, or any other ``compas_eve`` transport, such as
            ``compas_eve.mqtt.MqttTransport``, to reach a driver over MQTT.
        namespace : :obj:`str`
            Namespace to allow multiple robots to be controlled through the same connection.
            Optional. If not specified, it will use namespace ``/rob1``.
        """
        self.transport = _as_transport(transport)
        self.ros = self.transport
        self.counter = SequenceCounter()
        if not namespace.endswith("/"):
            namespace += "/"
        self.namespace = namespace
        self._version_checked = False
        self._protocol_version_known = threading.Event()
        self._protocol_version: Optional[int] = None
        self._protocol_version_error: Optional[Exception] = None

        self._publisher = Publisher(
            _robot_message_topic(self.transport, namespace + "robot_command", queue_size=None),
            transport=self.transport,
        )
        self._subscriber = Subscriber(
            _robot_message_topic(self.transport, namespace + "robot_response", queue_size=0),
            callback=self.feedback_callback,
            transport=self.transport,
        )
        self._subscriber.subscribe()
        self._publisher.advertise()
        self.futures: Dict[str, Dict[str, Any]] = {}

        threading.Thread(target=self.version_check, daemon=True).start()

    def version_check(self) -> None:
        """Check if the protocol version on the server matches the protocol version on the client.

        This runs on a background thread, so any failure is captured and
        re-raised from :meth:`ensure_protocol_version`, where the caller can see it.
        """
        try:
            version = self._read_announced_protocol_version()

            if version is None:
                version = self._read_protocol_version_parameter()

            self._protocol_version = version
        except Exception as exception:  # noqa: BLE001
            self._protocol_version_error = exception
        finally:
            self._protocol_version_known.set()

    def _read_announced_protocol_version(self) -> Optional[int]:
        """Read the protocol version the driver announces on a retained topic.

        The driver publishes its protocol version on ``<namespace>/protocol_version``,
        latched on ROS and retained on MQTT, so a client that connects at any
        point still receives it. This is the only mechanism that works on every
        transport.
        """
        received = []
        announced = threading.Event()

        def _on_version(message: FeedbackMessage) -> None:
            received.append(message["data"])
            announced.set()

        subscriber = Subscriber(
            _protocol_version_topic(self.transport, self.namespace + PROTOCOL_VERSION_TOPIC),
            callback=_on_version,
            transport=self.transport,
        )
        subscriber.subscribe()

        try:
            if not announced.wait(PROTOCOL_VERSION_TIMEOUT):
                return None
            return int(received[0])
        finally:
            subscriber.unsubscribe()

    def _read_protocol_version_parameter(self) -> int:
        """Read the protocol version from the ROS parameter server.

        Drivers that do not yet announce their version on a topic only expose it
        as a ROS parameter, so this is used as a fallback. It is not available on
        transports other than ROS.
        """
        if not isinstance(self.transport, RosTransport):
            raise Exception("The driver did not announce its protocol version on {}{} within {} seconds.".format(self.namespace, PROTOCOL_VERSION_TOPIC, PROTOCOL_VERSION_TIMEOUT))

        client = self.transport.client
        version = roslibpy.Param(client, self.namespace + PROTOCOL_VERSION_TOPIC).get()

        # No version is usually caused by wrong namespace in the connection, check that and raise correct error
        if version is None:
            params = client.get_params()

            detected_namespaces = set()
            tentative_namespaces = set()
            for param in params:
                if param.endswith("/robot_state_port") or param.endswith("/protocol_version"):
                    namespace = param[: param.rindex("/")]
                    if namespace not in tentative_namespaces:
                        tentative_namespaces.add(namespace)
                    else:
                        detected_namespaces.add(namespace)

            raise Exception("Cannot find the specified namespace. Detected namespaces={}".format(sorted(detected_namespaces)))

        return version

    def ensure_protocol_version(self) -> None:
        """Ensure protocol version on the server matches the protocol version on the client."""
        if self._version_checked:
            return

        if not self._protocol_version:
            # The check itself waits up to PROTOCOL_VERSION_TIMEOUT for the
            # announcement before falling back, so allow for both steps here.
            if not self._protocol_version_known.wait(2 * PROTOCOL_VERSION_TIMEOUT):
                raise Exception("Could not yet retrieve server protocol version")

        if self._protocol_version_error:
            raise self._protocol_version_error

        if self._protocol_version != CLIENT_PROTOCOL_VERSION:
            raise Exception("Protocol version mismatch. Server={}, Client={}".format(self._protocol_version, CLIENT_PROTOCOL_VERSION))

        self._version_checked = True

    def close(self) -> None:
        """Stop publishing and listening on the robot topics."""
        self._publisher.unadvertise()
        self._subscriber.unsubscribe()
        time.sleep(0.5)

    def _disconnect_topics(self) -> None:
        """Deprecated alias of :meth:`close`."""
        self.close()

    def send(self, instruction: Instruction) -> Optional[FutureResult]:
        """Sends an instruction to the robot without waiting.

        Instructions can indicate that feedback is required or not. If
        the instruction sent does not require feedback, this method
        returns ``None``. However, if the instruction needs
        feedback (i.e. ``feedback_level`` is greater than zero), the method
        returns a future result object that can be used to wait for completion.

        Waiting for a future can be done immediately after calling this, or
        deferred to a later point.

        Parameters
        ----------
        instruction : :class:`compas_rrc.Instruction`
            Instruction to send to the robot.

        Returns
        -------
        :class:`FutureResult`:
            Represent the future value of the feedback request. This method
            will return immediately, and this object can be used to wait or
            react to the feedback whenever it becomes available.

        Examples
        --------

        Streaming commands without blocking or waiting for feedback::

            # Print path
            abb.send(rrc.MoveToFrame(Frame.worldXY(), 150, rrc.Zone.FINE, rrc.Motion.LINEAR))

        Send commands and defer waiting to a future point in time::

            # Stop watch
            done = abb.send_and_wait(rrc.StopWatch())

            # Read watch
            future = abb.send(rrc.ReadWatch())

            # Move robot to end position
            abb.send(rrc.MoveToJoints(robot_joints_end_position, external_axis_dummy, 1000, rrc.Zone.FINE))

            # Read and print printing time
            watch_time = future.result(timeout=3.0)
            print('Print Time [s] = ', watch_time)

        """
        self.ensure_protocol_version()
        instruction.sequence_id = self.counter.increment()

        key = _get_key(instruction)
        result = None

        if instruction.feedback_level > 0:
            result = FutureResult()
            parser = instruction.parse_feedback if hasattr(instruction, "parse_feedback") else None
            self.futures[key] = dict(result=result, parser=parser)

        self._publisher.publish(instruction.msg)

        return result

    def send_and_wait(self, instruction: Instruction, timeout: Optional[float] = None) -> Any:
        """Send instruction and wait for feedback.

        This is a blocking call, it will only return once the robot
        sends the requested feedback. If ``feedback_level``
        of the ``instruction`` parameter is ``0``, it will be automatically
        set to ``1``.

        Parameters
        ----------
        instruction : :class:`compas_rrc.Instruction`
            Instruction to send to the robot.
        timeout : :obj:`int`
            Timeout in seconds to wait before raising an exception. Optional.

        Returns
        -------
        object
            Returns the feedback value that resulted from the execution of the instruction.

        Examples
        --------

        Send an instruction and wait for feedback from the robot. In the following example,
        the code will not continue until the robot has started to execute this instruction.
        On move instructions, a ``Zone.FINE`` can be used to make sure the motion planner has
        executed the instruction fully::

            # Move robot to start position
            done = abb.send_and_wait(rrc.MoveToJoints(robot_joints_start_position, external_axis_dummy, 1000, rrc.Zone.FINE))

        """
        if instruction.feedback_level == 0:
            instruction.feedback_level = 1

        future = self.send(instruction)

        if future is None:
            raise InstructionException("Instruction did not produce a future result", instruction)

        return future.result(timeout)

    def send_and_subscribe(self, instruction: Instruction, callback: Callable[[Any], None]) -> None:
        """Send instruction and activate a service on the robot to stream feedback at a regular inverval.

        Parameters
        ----------
        instruction : :class:`compas_rrc.Instruction`
            Instruction to send to the robot.
        callback
            Python function to be invoked every time a new value is made available.

        Notes
        -----
            This feature is currently only usable with custom instructions.

        """
        self.ensure_protocol_version()
        instruction.sequence_id = self.counter.increment()

        key = _get_key(instruction)

        parser = instruction.parse_feedback if hasattr(instruction, "parse_feedback") else None
        self.futures[key] = dict(callback=callback, parser=parser)

        self._publisher.publish(instruction.msg)

    def feedback_callback(self, message: FeedbackMessage) -> None:
        """Internal method."""
        response_key = _get_response_key(message)
        future = self.futures.get(response_key, None)

        if future:
            if future["parser"]:
                result = future["parser"](message)
            else:
                result = default_feedback_parser(message)
            if "result" in future:
                future["result"]._set_result(result)
                self.futures.pop(response_key)
            elif "callback" in future:
                future["callback"](result)
                # TODO: Handle unsubscribes
