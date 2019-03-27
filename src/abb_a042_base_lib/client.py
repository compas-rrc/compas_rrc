import json
import time
import threading
import roslibpy


class AbbClient(object):
    """ROS-based ABB Client."""
    def __init__(self, ros):
        self.ros = ros
        self.service = roslibpy.Service(ros, '/abb_command', 'abb_042_driver/AbbStringCommand')
        self.topic = roslibpy.Topic(ros, '/abb_command', 'abb_042_driver/AbbMessage')
        self.topic.advertise()
        time.sleep(0.5)

    def run(self):
        self.ros.run()

    def run_forever(self):
        self.ros.run_forever()

    def terminate(self):
        self.ros.terminate()

    def send(self, instruction):
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

        event = threading.Event()
        context = {}

        def service_response(result):
            print(result)
            context['response'] = json.loads(result['response'])
            event.set()

        def service_err(*exception):
            context['exception'] = exception
            event.set()

        self.service.call(roslibpy.ServiceRequest({'command': json.dumps(instruction.msg)}), service_response, service_err)
        event.wait()

        if 'exception' in context:
            raise context['exception']

        return context['response']
