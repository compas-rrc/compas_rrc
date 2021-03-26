import threading
import time

import roslibpy
from compas_fab.backends import RosClient

from .common import CLIENT_PROTOCOL_VERSION
from .common import FutureResult
from .common import InstructionException

__all__ = ['RosClient', 'AbbClient']


FEEDBACK_ERROR_PREFIX = 'Done FError '


def _get_key(message):
    return 'msg:{}'.format(message.sequence_id)


def _get_response_key(message):
    return 'msg:{}'.format(message['feedback_id'])


class SequenceCounter(object):
    """An atomic, thread-safe sequence increament counter."""

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
            return self._value

    @property
    def value(self):
        """Current sequence counter."""
        with self._lock:
            return self._value


def default_feedback_parser(result):
    feedback_value = result['feedback']

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

    def __init__(self, ros, namespace='/rob1'):
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
        self.counter = SequenceCounter()
        if not namespace.endswith('/'):
            namespace += '/'
        self._version_checked = False
        self._server_protocol_check = dict(event=threading.Event(),
                                           param=roslibpy.Param(ros, namespace + 'protocol_version'),
                                           version=None)
        self.ros.on_ready(self.version_check)
        self.topic = roslibpy.Topic(ros, namespace + 'robot_command', 'compas_rrc_driver/RobotMessage', queue_size=None)
        self.feedback = roslibpy.Topic(ros, namespace + 'robot_response', 'compas_rrc_driver/RobotMessage', queue_size=0)
        self.feedback.subscribe(self.feedback_callback)
        self.topic.advertise()
        self.futures = {}

        self.ros.on('closing', self._disconnect_topics)

    def version_check(self):
        """Check if the protocol version on the server matches the protocol version on the client."""
        self._server_protocol_check['version'] = self._server_protocol_check['param'].get()
        self._server_protocol_check['event'].set()

    def ensure_protocol_version(self):
        """Ensure protocol version on the server matches the protocol version on the client."""
        if self._version_checked:
            return

        if not self._server_protocol_check['version']:
            if not self._server_protocol_check['event'].wait(10):
                raise Exception('Could not yet retrieve server protocol version')

        if self._server_protocol_check['version'] != CLIENT_PROTOCOL_VERSION:
            raise Exception('Protocol version mismatch. Server={}, Client={}'.format(self._server_protocol_check['version'], CLIENT_PROTOCOL_VERSION))

        self._version_checked = True

    def _disconnect_topics(self):
        self.topic.unadvertise()
        self.feedback.unsubscribe()
        time.sleep(0.5)

    def send(self, instruction):
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
        instruction : :class:`compas_fab.backends.ros.messages.ROSmsg`
            ROS Message representing the instruction to send.

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
            parser = instruction.parse_feedback if hasattr(instruction, 'parse_feedback') else None
            self.futures[key] = dict(result=result, parser=parser)

        self.topic.publish(roslibpy.Message(instruction.msg))

        return result

    def send_and_wait(self, instruction, timeout=None):
        """Send instruction and wait for feedback.

        This is a blocking call, it will only return once the robot
        sends the requested feedback. If ``feedback_level``
        of the ``instruction`` parameter is ``0``, it will be automatically
        set to ``1``.

        Parameters
        ----------
        instruction : :class:`compas_fab.backends.ros.messages.ROSmsg`
            ROS Message representing the instruction to send.
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
        return future.result(timeout)

    def send_and_subscribe(self, instruction, callback):
        """Send instruction and activate a service on the robot to stream feedback at a regular inverval.

        Parameters
        ----------
        instruction : :class:`compas_fab.backends.ros.messages.ROSmsg`
            ROS Message representing the instruction to send.
        callback
            Python function to be invoked every time a new value is made available.

        Notes
        -----
            This feature is currently only usable with custom instructions.

        """
        self.ensure_protocol_version()
        instruction.sequence_id = self.counter.increment()

        key = _get_key(instruction)

        parser = instruction.parse_feedback if hasattr(instruction, 'parse_feedback') else None
        self.futures[key] = dict(callback=callback, parser=parser)

        self.topic.publish(roslibpy.Message(instruction.msg))

    def feedback_callback(self, message):
        """Internal method."""
        response_key = _get_response_key(message)
        future = self.futures.get(response_key, None)

        if future:
            result = message
            if future['parser']:
                result = future['parser'](result)
            else:
                result = default_feedback_parser(result)
            if 'result' in future:
                future['result']._set_result(result)
                self.futures.pop(response_key)
            elif 'callback' in future:
                future['callback'](result)
                # TODO: Handle unsubscribes
