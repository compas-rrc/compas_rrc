import json
import time
import threading
import roslibpy

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
    counter = SequenceCounter()

    """ROS-based ABB Client."""
    def __init__(self, ros):
        self.ros = ros
        self.topic = roslibpy.Topic(ros, '/abb_command', 'abb_042_driver/AbbMessage')
        self.feedback = roslibpy.Topic(ros, '/abb_response', 'abb_042_driver/AbbMessage')
        self.feedback.subscribe(self.feedback_callback)
        self.topic.advertise()
        self.wait_events = {}
        time.sleep(0.5)

    def run(self):
        self.ros.run()

    def run_forever(self):
        self.ros.run_forever()

    def close(self):
        self.topic.unadvertise()
        self.feedback.unsubscribe()
        time.sleep(1)

        self.ros.close()

    def terminate(self):
        self.ros.terminate()

    def send(self, instruction):
        # if not hasattr(instruction, 'sequence_id') or not instruction.sequence_id:
        instruction.sequence_id = AbbClient.counter.increment()
        self.topic.publish(roslibpy.Message(instruction.msg))

    def send_and_wait(self, instruction):
        """Send instruction and wait for feedback.

        This is a blocking call, it will only return once the ABB client
        send the requested feedback. For this reason, the ``feedback_level``
        of the ``instruction`` parameter needs to be greater than zero.

        Args:
            instruction:
                ROS Message representing the instruction to send.

        """
        if instruction.feedback_level == 0:
            raise ValueError('Feedback level needs to be greater than zero')

        instruction.sequence_id = AbbClient.counter.increment()

        event = threading.Event()
        self.wait_events[_get_key(instruction)] = event

        # def instruction_response(result):
        #     print(result)
        #     context['response'] = json.loads(result['response'])
        #     event.set()

        self.topic.publish(roslibpy.Message(instruction.msg))
        event.wait()

    def feedback_callback(self, message):
        response_key = _get_response_key(message)
        event = self.wait_events.get(response_key)
        if event:
            event.set()
