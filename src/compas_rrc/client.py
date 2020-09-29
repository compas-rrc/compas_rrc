import threading
import time

import roslibpy

from .common import CLIENT_PROTOCOL_VERSION
from .common import FutureResult
from .common import InstructionException

__all__ = ['AbbClient']


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

    >>> from compas_fab.backends import RosClient
    >>> from compas_rrc import *
    >>> ros = RosClient()
    >>> abb = AbbClient(ros)
    >>> abb.run()
    >>> abb.ros.is_connected
    True
    >>> abb.close()

    """

    def __init__(self, ros, namespace='/'):
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
        self.feedback = roslibpy.Topic(ros, namespace + 'robot_response', 'compas_rrc_driver/RobotMessage')
        self.feedback.subscribe(self.feedback_callback)
        self.topic.advertise()
        self.futures = {}

    def version_check(self):
        self._server_protocol_check['version'] = self._server_protocol_check['param'].get()
        self._server_protocol_check['event'].set()

    def ensure_protocol_version(self):
        if self._version_checked:
            return

        if not self._server_protocol_check['version']:
            if not self._server_protocol_check['event'].wait(10):
                raise Exception('Could not yet retrieve server protocol version')

        if self._server_protocol_check['version'] != CLIENT_PROTOCOL_VERSION:
            raise Exception('Protocol version mismatch. Server={}, Client={}'.format(self._server_protocol_check['version'], CLIENT_PROTOCOL_VERSION))

        self._version_checked = True

    def run(self, timeout=None):
        """Starts the event loop in a thread."""
        self.ros.run(timeout)

    def run_forever(self):
        """Starts the event loop and blocks."""
        self.ros.run_forever()

    def close(self):
        """Close the connection to the robot."""
        self.topic.unadvertise()
        self.feedback.unsubscribe()

        # Give it a bit of time to unsubscribe
        time.sleep(1)

        self.ros.close()

    def terminate(self):
        """Terminate the event loop that controls the connection.

        Once terminated, the program must exit, as the underlying event-loop
        cannot be restarted."""
        self.ros.terminate()

    def send(self, instruction):
        """Sends an instruction to the robot without waiting.

        Instructions can indicate that feedback is required or not. If
        the instruction sent does not require feedback, this method
        returns ``None``. However, if the instruction needs
        feedback (i.e. ``feedback_level`` is greater than zero), the method
        returns a future result object that can be used to wait for completion.

        Returns: :class:`FutureResult`
            Represent the future value of the feedback request. This method
            will return immediately, and this object can be used to wait or
            react to the feedback whenever it becomes available.

        Args:
            instruction: ROS Message representing the instruction to send.

        Returns:
            :class:`FutureResult`: If ``feedback_level`` is greater than zero,
            the return is a future object that allows to defer waiting for
            results.
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

        This is a blocking call, it will only return once the client
        send the requested feedback. For this reason, the ``feedback_level``
        of the ``instruction`` parameter needs to be greater than zero.

        Args:
            instruction: ROS Message representing the instruction to send.
            timeout (int): Timeout in seconds to wait before raising an exception. Optional.
        """
        if instruction.feedback_level == 0:
            instruction.feedback_level = 1

        future = self.send(instruction)
        return future.result(timeout)

    def send_and_subscribe(self, instruction, callback):
        self.ensure_protocol_version()
        instruction.sequence_id = self.counter.increment()

        key = _get_key(instruction)

        parser = instruction.parse_feedback if hasattr(instruction, 'parse_feedback') else None
        self.futures[key] = dict(callback=callback, parser=parser)

        self.topic.publish(roslibpy.Message(instruction.msg))

    def feedback_callback(self, message):
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
