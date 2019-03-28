
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
    """Represents valid feedback levels for motion instructions."""
    NONE = 0
    DONE = 1


class MoveAbsJ(ROSmsg):
    """Represents a move absolute joint instruction.

    Attributes:

        joints (:obj:`list` of :obj:`float`):
            Joint positions in degrees.

        ext_axes (:obj:`list` of :obj:`float`):
            External axes positions, depending on the robotic system,
            it can be millimeters for prismatic external axes,
            or degrees for revolute external axes.

        speed (:obj:`int`):
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.

        zone (:class:`Zone`):
            Zone data. Predefined in the robot contrller,
            only Zone ``fine`` will do a stop point all others are fly by points

        feedback_level (:obj:`int`):
            Integer specifying requested feedback level. Default=``0`` (i.e. ``NONE``).
            Feedback level is instruction-specific but the value ``1`` always represents
            completion of the instruction.


    ABB Documentation - Usage:

        MoveAbsJ (Move Absolute Joint) is used to move the robot and external axes to
        an absolute position defined in axes positions.

        The final position of the robot during a movement with MoveAbsJ is neither affected
        by the given tool and work object nor by active program displacement. The robot
        uses this data to calculate the load, TCP velocity, and the corner path. The same
        tools can be used in adjacent movement instructions.
        The robot and external axes move to the destination position along a non-linear
        path. All axes reach the destination position at the same time.
        This instruction can only be used in the main task T_ROB1 or, if in a MultiMove
        system, in Motion tasks.
    """

    def __init__(self, joints, ext_axes, speed, zone, feedback_level=MotionFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'MoveAbsJ'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT

        joints = joints or []
        if len(joints) > 6:
            raise ValueError('Only up to 6 joints are supported')
        joints_pad = [0.0] * (6 - len(joints))

        ext_axes = ext_axes or []
        if len(ext_axes) > 6:
            raise ValueError('Only up to 6 external axes are supported')

        ext_axes_pad = [0.0] * (6 - len(ext_axes))
        self.string_values = []
        self.float_values = joints + joints_pad + ext_axes + ext_axes_pad + [speed, zone]


class MoveJ(ROSmsg):
    """Represents a move joint instruction.

    Attributes:

        pos (:obj:`list` of :obj:`float`):
            Translation X, Y and Z positions in milimeters.

        rot (:obj:`list` of :obj:`float`):
            Rotation Q1, Q2, Q3 and Q4 in quatarnions.

        ext_axes (:obj:`list` of :obj:`float`):
            External axes positions, depending on the robotic system,
            it can be millimeters for prismatic external axes,
            or degrees for revolute external axes.

        speed (:obj:`int`):
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.

        zone (:class:`Zone`):
            Zone data. Predefined in the robot contrller,
            only Zone ``fine`` will do a stop point all others are fly by points

        feedback_level (:obj:`int`):
            Integer specifying requested feedback level. Default=``0`` (i.e. ``NONE``).
            Feedback level is instruction-specific but the value ``1`` always represents
            completion of the instruction.


    ABB Documentation - Usage:

        MoveJ is used to move the robot quickly from one point to another when that
        movement does not have to be in a straight line.
        The robot and external axes move to the destination position along a non-linear
        path. All axes reach the destination position at the same time.
        This instruction can only be used in the main task T_ROB1 or, if in a MultiMove
        system, in Motion tasks.

    """

    def __init__(self, pos, rot, ext_axes, speed, zone, feedback_level=MotionFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'MoveJ'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT

        pos = pos or []
        if len(pos) != 3:
            raise ValueError('X, Y, Z, values are needed')

        rot = rot or []
        if len(rot) != 4:
            raise ValueError('Q1, Q2, Q3, Q4 values are needed')
        # maybe check the quartinions sum ?

        ext_axes = ext_axes or []
        if len(ext_axes) > 6:
            raise ValueError('Only up to 6 external axes are supported')
        ext_axes_pad = [0.0] * (6 - len(ext_axes))

        self.string_values = []
        self.float_values = pos + rot + ext_axes + ext_axes_pad + [speed, zone]


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
