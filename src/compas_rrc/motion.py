from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

INSTRUCTION_PREFIX = 'r_A042_'

__all__ = [
    'Zone',
    'Motion',
    'MoveToJoints',
    'MoveToFrame',
    'MoveToRobtarget',
]


class Zone(object):
    """Describes the valid zone data definitions."""
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


class Motion(object):
    """Describes the valid motion types."""
    LINEAR = 'L'
    JOINT = 'J'


class MoveToJoints(ROSmsg):
    """Move to configuration is a call that moves the robot with axis values.

    RAPID Instruction: ``MoveAbsJ``

    Attributes:

        joints (:class:`compas_rrc.common.RobotJoints` or :obj:`list` of :obj:`float`):
            Robot joint positions.

        ext_axes (:class:`compas_rrc.common.ExternalAxes` or :obj:`list` of :obj:`float`):
            External axes positions.

        speed (:obj:`int`):
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.

        zone (:class:`Zone`):
            Zone data. Predefined in the robot contrller,
            only Zone ``fine`` will do a stop point all others are fly by points

        feedback_level (:obj:`int`):
            Integer specifying requested feedback level. Default=``0`` (i.e. ``NONE``).
            Feedback level is instruction-specific but the value ``1`` always represents
            completion of the instruction.
    """

    def __init__(self, joints, ext_axes, speed, zone, feedback_level=FeedbackLevel.NONE):
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
        self.float_values = list(joints) + joints_pad + list(ext_axes) + ext_axes_pad + [speed, zone]


class MoveGeneric(ROSmsg):
    def __init__(self, frame, ext_axes, speed, zone, feedback_level=FeedbackLevel.NONE):
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT

        pos = list(frame.point)
        rot = list(frame.quaternion)

        ext_axes = ext_axes or []
        if len(ext_axes) > 6:
            raise ValueError('Only up to 6 external axes are supported')
        ext_axes_pad = [0.0] * (6 - len(ext_axes))

        self.string_values = []
        self.float_values = pos + rot + list(ext_axes) + ext_axes_pad + [speed, zone]


class MoveToFrame(MoveGeneric):
    """Move to frame is a call that moves the robot in the cartisian space.

    RAPID Instruction: MoveJ or MoveL

    -- old Text --
    Represents a move joint instruction.

    Attributes:

        frame (:class:`compas.geometry.Frame`):
            Target frame.

        speed (:obj:`int`):
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.

        zone (:class:`Zone`):
            Zone data. Predefined in the robot contrller,
            only Zone ``fine`` will do a stop point all others are fly by points

        motion_type (:class:`Motion`):
            Motion type. Defaults to Joint.

        feedback_level (:obj:`int`):
            Integer specifying requested feedback level. Default=``0`` (i.e. ``NONE``).
            Feedback level is instruction-specific but the value ``1`` always represents
            completion of the instruction.

    Note
    ----

        ABB Documentation - Usage:

        MoveJ is used to move the robot quickly from one point to another when that
        movement does not have to be in a straight line.
        The robot and external axes move to the destination position along a non-linear
        path. All axes reach the destination position at the same time.
        This instruction can only be used in the main task T_ROB1 or, if in a MultiMove
        system, in Motion tasks.

    """

    def __init__(self, frame, speed, zone, motion_type=Motion.JOINT, feedback_level=FeedbackLevel.NONE):
        super(MoveToFrame, self).__init__(frame, [], speed, zone, feedback_level)
        instruction = 'MoveToFrameJ' if motion_type == Motion.JOINT else 'MoveToFrameL'
        self.instruction = INSTRUCTION_PREFIX + instruction


class MoveToRobtarget(MoveGeneric):
    """Move to frame is a call that moves the robot in the cartisian space.

    RAPID Instruction: ``MoveJ`` or ``MoveL``

    Attributes:

        frame (:class:`compas.geometry.Frame`):
            Target frame.

        ext_axes (:class:`compas_rrc.common.ExternalAxes` or :obj:`list` of :obj:`float`):
            External axes positions.

        speed (:obj:`int`):
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.

        zone (:class:`Zone`):
            Zone data. Predefined in the robot controller,
            only Zone ``fine`` will do a stop point all others are fly by points

        motion_type (:class:`Motion`):
            Motion type. Defaults to Joint.

        feedback_level (:obj:`int`):
            Integer specifying requested feedback level. Default=``0`` (i.e. ``NONE``).
            Feedback level is instruction-specific but the value ``1`` always represents
            completion of the instruction.

    """

    def __init__(self, frame, ext_axes, speed, zone, motion_type=Motion.JOINT, feedback_level=FeedbackLevel.NONE):
        super(MoveToRobtarget, self).__init__(frame, ext_axes, speed, zone, feedback_level)
        instruction = 'MoveJ' if motion_type == Motion.JOINT else 'MoveL'
        self.instruction = INSTRUCTION_PREFIX + instruction
