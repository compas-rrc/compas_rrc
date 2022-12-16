import functools
import threading
import time

import roslibpy
from compas_fab.backends import RosClient

from .common import CLIENT_PROTOCOL_VERSION
from .common import FutureResult
from .common import InstructionException
from .common import Interfaces

__all__ = ["RosClient", "AbbClient"]


FEEDBACK_ERROR_PREFIX = "Done FError "


def _get_key(message):
    prefix = "sys" if message.meta["interface"] == Interfaces.SYS else "msg"
    return "{}:{}".format(prefix, message.sequence_id)


def _get_response_key(message, prefix):
    return "{}:{}".format(prefix, message["feedback_id"])


class SequenceCounter(object):
    """An atomic, thread-safe sequence increament counter."""

    ROLLOVER_THRESHOLD = 1000000

    def __init__(self, start=0):
        """Initialize a new counter to given initial value."""
        self._lock = threading.Lock()
        self._value = start

    def increment(self, num=1):
        """Atomically increment the counter by ``num`` and
        return the new value.
        """
        with self._lock:
            self._value += num
            if self._value > SequenceCounter.ROLLOVER_THRESHOLD:
                self._value = 1
            return self._value

    @property
    def value(self):
        """Current sequence counter."""
        with self._lock:
            return self._value


def default_feedback_parser(result):
    feedback_value = result["feedback"]

    if feedback_value.startswith(FEEDBACK_ERROR_PREFIX):
        return InstructionException(feedback_value, result)

    return feedback_value


class AbbClient(object):
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

    def __init__(self, ros, namespace="/rob1"):
        """Initialize a new robot client instance.

        Parameters
        ----------
        ros : :class:`RosClient`
            Instance of a ROS connection.
        namespace : :obj:`str`
            Namespace to allow multiple robots to be controlled through the same ROS instance.
            Optional. If not specified, it will use namespace ``/rob1``.
        """
        self.ros = ros

        # Interface-specific counters
        self.counters = {}
        self.counters[Interfaces.APP] = SequenceCounter()
        self.counters[Interfaces.SYS] = SequenceCounter()

        if not namespace.endswith("/"):
            namespace += "/"
        self._version_checked = False
        self._server_protocol_check = dict(
            event=threading.Event(), param=roslibpy.Param(ros, namespace + "protocol_version"), version=None
        )
        self.ros.on_ready(self.version_check)

        # Interface-specific communication channels
        self.topics = {}
        self.feedback_topics = {}

        # Main communication channel
        self.topics[Interfaces.APP] = roslibpy.Topic(
            ros, namespace + "robot_command", "compas_rrc_driver/RobotMessage", queue_size=None
        )
        self.feedback_topics[Interfaces.APP] = roslibpy.Topic(
            ros, namespace + "robot_response", "compas_rrc_driver/RobotMessage", queue_size=0
        )
        self.feedback_topics[Interfaces.APP].subscribe(functools.partial(self.feedback_callback, key_prefix="msg"))

        # System communication channel
        self.topics[Interfaces.SYS] = roslibpy.Topic(
            ros, namespace + "robot_command_system", "compas_rrc_driver/RobotMessage", queue_size=None
        )
        self.feedback_topics[Interfaces.SYS] = roslibpy.Topic(
            ros, namespace + "robot_response_system", "compas_rrc_driver/RobotMessage", queue_size=0
        )
        self.feedback_topics[Interfaces.SYS].subscribe(functools.partial(self.feedback_callback, key_prefix="sys"))

        for topic in self.topics.values():
            topic.advertise()

        self.futures = {}

        self.ros.on("closing", self._disconnect_topics)

    def version_check(self):
        """Check if the protocol version on the server matches the protocol version on the client."""
        self._server_protocol_check["version"] = self._server_protocol_check["param"].get()
        # No version is usually caused by wrong namespace in the connection, check that and raise correct error
        if self._server_protocol_check["version"] is None:
            params = self.ros.get_params()

            detected_namespaces = set()
            tentative_namespaces = set()
            for param in params:
                if param.endswith("/robot_state_port") or param.endswith("/protocol_version"):
                    namespace = param[: param.rindex("/")]
                    if namespace not in tentative_namespaces:
                        tentative_namespaces.add(namespace)
                    else:
                        detected_namespaces.add(namespace)

            raise Exception(
                "Cannot find the specified namespace. Detected namespaces={}".format(sorted(detected_namespaces))
            )

        self._server_protocol_check["event"].set()

    def ensure_protocol_version(self):
        """Ensure protocol version on the server matches the protocol version on the client."""
        if self._version_checked:
            return

        if not self._server_protocol_check["version"]:
            if not self._server_protocol_check["event"].wait(10):
                raise Exception("Could not yet retrieve server protocol version")

        if self._server_protocol_check["version"] != CLIENT_PROTOCOL_VERSION:
            raise Exception(
                "Protocol version mismatch. Server={}, Client={}".format(
                    self._server_protocol_check["version"], CLIENT_PROTOCOL_VERSION
                )
            )

        self._version_checked = True

    def _disconnect_topics(self):
        for topic in self.topics.values():
            topic.unadvertise()
        for topic in self.feedback_topics.values():
            topic.unadvertise()
        time.sleep(0.5)

    def send(self, instruction, interface=None):
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
        instruction : :class:`compas_rrc.BaseInstruction`
            Instance of an instruction to send.
        interface :class:`compas_rrc.Interfaces`
            Select the interface over which the instruction will be sent.
            Defaults to ``Interfaces.APP`` unless the instruction has another default.

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
        result = None

        interface = interface or instruction.meta.get("interface") or Interfaces.APP
        instruction.select_interface(interface)

        counter = self.counters[interface]
        topic = self.topics[interface]

        instruction.sequence_id = counter.increment()
        key = _get_key(instruction)

        # NOTE: create a base class for all instructions (system and standard)
        # and add a method .produces_feedback() (or similar) that determines
        # the conditions under which the instruction will need the future result handling
        if instruction.feedback_level > 0 or instruction.feedback_level == -1:
            result = FutureResult()
            parser = instruction.parse_feedback if hasattr(instruction, "parse_feedback") else None
            self.futures[key] = dict(result=result, parser=parser)

        topic.publish(instruction.to_message())

        return result

    def send_and_wait(self, instruction, timeout=None, interface=None):
        """Send instruction and wait for feedback.

        This is a blocking call, it will only return once the robot
        sends the requested feedback. If ``feedback_level``
        of the ``instruction`` parameter is ``0``, it will be automatically
        set to ``1``.

        Parameters
        ----------
        instruction : :class:`compas_rrc.BaseInstruction`
            Instance of an instruction to send.
        timeout : :obj:`int`
            Timeout in seconds to wait before raising an exception. Optional.
        interface :class:`compas_rrc.Interfaces`
            Select the interface over which the instruction will be sent.
            Defaults to ``Interfaces.APP`` unless the instruction has another default.

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
            if instruction.exec_level == -1:
                instruction.feedback_level = -1
            else:
                instruction.feedback_level = 1

        future = self.send(instruction, interface)
        return future.result(timeout)

    def send_and_subscribe(self, instruction, callback, interface=None):
        """Send instruction and activate a service on the robot to stream feedback at a regular inverval.

        Parameters
        ----------
        instruction : :class:`compas_rrc.BaseInstruction`
            Instance of an instruction to send.
        callback
            Python function to be invoked every time a new value is made available.
        interface :class:`compas_rrc.Interfaces`
            Select the interface over which the instruction will be sent.
            Currently only ``Interfaces.APP`` is supported.

        Notes
        -----
            This feature is currently only usable with custom instructions.

        """
        interface = interface or instruction.meta.get("interface") or Interfaces.APP
        if interface != Interfaces.APP:
            raise NotImplementedError("Not supported for now")

        self.ensure_protocol_version()
        instruction.sequence_id = self.counters[interface].increment()

        key = _get_key(instruction)

        parser = instruction.parse_feedback if hasattr(instruction, "parse_feedback") else None
        self.futures[key] = dict(callback=callback, parser=parser)

        self.topics[interface].publish(instruction.to_message())

    def feedback_callback(self, message, key_prefix):
        """Internal method."""
        response_key = _get_response_key(message, key_prefix)
        future = self.futures.get(response_key, None)

        if future:
            result = message
            if future["parser"]:
                result = future["parser"](result)
            else:
                result = default_feedback_parser(result)
            if "result" in future:
                future["result"]._set_result(result)
                self.futures.pop(response_key)
            elif "callback" in future:
                future["callback"](result)
                # TODO: Handle unsubscribes
