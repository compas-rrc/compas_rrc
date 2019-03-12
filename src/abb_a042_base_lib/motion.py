
from compas_fab.backends.ros.messages import ROSmsg

INSTRUCTION_PREFIX = 'r_A042_'


class ExecutionLevel(object):
    ROBOT = 0
    RECEIVER = 1
    SENDER = 2
    MASTER = 10


class Zone(object):
    FINE = -1
    Z0 = 0
    Z1 = 1
    Z5 = 5
    Z10 = 10
    Z15 = 15
    Z20 = 20
    Z30 = 30
    Z40 = 40
    Z50 = 50
    Z60 = 60
    Z80 = 80
    Z100 = 100
    Z150 = 150
    Z200 = 200


class MotionFeedback(object):
    NONE = 0
    DONE = 1


class MoveAbsJ(ROSmsg):
    """Represents a move absolute joint instruction.

    Attributes:
        joints (:obj:`list` of :obj:`float`): Joint positions in degrees.
        ext_axes (:obj:`list` of :obj:`float`): External axes positions, depending
            on the robotic system, it can be millimeters for prismatic external axes, or
            degrees for revolute external axes.
        speed (:obj:`int`): Integer specifying translational speed in mm/s. Min=``0.01``.
        zone (:class:`Zone`): Zone data.
    """

    def __init__(self, joints, ext_axes, speed, zone, feedback_level=MotionFeedback.NONE):
        if len(joints) != 6:
            raise ValueError('Only 6 joints are supported')

        self.instruction = INSTRUCTION_PREFIX + 'MoveAbsJ'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT

        self.string_values = []
        self.float_values = joints + ext_axes + [speed, zone]


if __name__ == '__main__':
    import time
    import roslibpy

    print('Start test')

    ros = roslibpy.Ros('127.0.0.1', 9090)
    topic = roslibpy.Topic(ros, '/abb_command', 'abb_042_driver/AbbMessage')
    topic.advertise()
    time.sleep(0.5)

    def send_test_instruction():
        # robjoints = [90, 45, 30, 0, 10, 20]
        # gantry_axis_x = 10000
        # gantry_axis_y = -5000
        # gantry_axis_z = -2000
        # speed = 200
        # zone = fine

        instruction = MoveAbsJ([90, 45, 34, 1, 10, 20], [10000, -5000, -2000], 200, Zone.FINE)
        print(instruction)
        topic.publish(roslibpy.Message(instruction.msg))

    ros.on_ready(send_test_instruction)
    ros.run_forever()
