import json
import threading
import time

import roslibpy
from .common import FutureResult

__all__ = ['AbbClient']

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


class AbbClient(object):
    """ROS ABB Client.

    This client handles all communication over ROS topics, and implements
    blocking behaviors as an application-level construct."""
    def __init__(self, ros, namespace='/'):
        self.ros = ros
        self.counter = SequenceCounter()
        if not namespace.endswith('/'):
            namespace += '/'
        self.topic = roslibpy.Topic(ros, namespace + 'robot_command', 'abb_042_driver/RobotMessage', queue_size=None)
        self.feedback = roslibpy.Topic(ros, namespace + 'robot_response', 'abb_042_driver/RobotMessage')
        self.feedback.subscribe(self.feedback_callback)
        self.topic.advertise()
        self.futures = {}

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
        instruction.sequence_id = self.counter.increment()

        key = _get_key(instruction)
        result = None

        if instruction.feedback_level > 0:
            result = FutureResult()
            self.futures[key] = result

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
            raise ValueError('Feedback level needs to be greater than zero')

        future = self.send(instruction)
        return future.result(timeout)

    def feedback_callback(self, message):
        response_key = _get_response_key(message)
        future = self.futures.pop(response_key, None)

        if future:
            future._set_result(message)
