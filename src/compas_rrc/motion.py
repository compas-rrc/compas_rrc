from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

INSTRUCTION_PREFIX = 'r_RRC_'

__all__ = [
    'Zone',
    'Motion',
    'MoveToJoints',
    'MoveToFrame',
    'MoveToRobtarget',
]


class Zone(object):
    """Describes the valid zone data definitions.

    There are two types of zones: fine and fly-by.
    If zone is ``FINE``, the movement terminates as a stop point, and the program execution
    will not continue until robot reach the stop point. For all other zones, the movement
    terminates as a fly-by point, and the program execution continues about 100 ms before
    the robot reaches the zone.

    .. autoattribute:: FINE
    .. autoattribute:: Z0
    .. autoattribute:: Z1
    .. autoattribute:: Z5
    .. autoattribute:: Z10
    .. autoattribute:: Z15
    .. autoattribute:: Z20
    .. autoattribute:: Z30
    .. autoattribute:: Z40
    .. autoattribute:: Z50
    .. autoattribute:: Z60
    .. autoattribute:: Z80
    .. autoattribute:: Z100
    .. autoattribute:: Z150
    .. autoattribute:: Z200

    """

    FINE = -1
    """
    Fine point.
    """

    Z0 = 0
    """
    0.3 mm.
    """

    Z1 = 1
    """
    1 mm.
    """

    Z5 = 5
    """
    5 mm.
    """

    Z10 = 10
    """
    10 mm.
    """

    Z15 = 15
    """
    15 mm.
    """

    Z20 = 20
    """
    20 mm.
    """

    Z30 = 30
    """
    30 mm.
    """

    Z40 = 40
    """
    40 mm.
    """

    Z50 = 50
    """
    50 mm.
    """

    Z60 = 60
    """
    60 mm.
    """

    Z80 = 80
    """
    80 mm.
    """

    Z100 = 100
    """
    100 mm.
    """

    Z150 = 150
    """
    150 mm.
    """

    Z200 = 200
    """
    200 mm.
    """


class Motion(object):
    """Represents valid motion types.

    .. autoattribute:: LINEAR
    .. autoattribute:: JOINT
    """
    LINEAR = 'L'
    """Moves the robot linearly to the specified position."""

    JOINT = 'J'
    """Moves the robot not linearly to the specified position by coordinating all joints to start and end together.
    This type of motion can be faster than LINEAR motion."""


class MoveToJoints(ROSmsg):
    """Move to joints is a call that moves the robot and the external axes with axes values.

    Examples
    --------
    .. code-block:: python

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(rrc.GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change value and move to new position
        robot_joints.rax_1 += 15
        speed = 100 # Unit [mm/s]
        done = abb.send_and_wait(rrc.MoveToJoints(robot_joints, external_axes, speed, rrc.Zone.FINE))

    RAPID Instruction: ``MoveAbsJ``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, joints, ext_axes, speed, zone, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        joints : :class:`compas_rrc.RobotJoints` or :obj:`list` of :obj:`float`
            Robot joint positions.
        ext_axes : :class:`compas_rrc.ExternalAxes` or :obj:`list` of :obj:`float`
            External axes positions.
        speed : :obj:`float`
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.
        zone : :class:`Zone`
            Zone data. Predefined in the robot controller,
            only Zone :attr:`Zone.FINE` will do a stop point all others are fly by points
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
            Use  :attr:`FeedbackLevel.DONE` and :attr:`Zone.FINE` together to make sure
            the motion planner has executed the instruction fully.
        """
        if speed <= 0:
            raise ValueError('Speed must be higher than zero. Current value={}'.format(speed))

        self.instruction = INSTRUCTION_PREFIX + 'MoveToJoints'
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
        if speed <= 0:
            raise ValueError('Speed must be higher than zero. Current value={}'.format(speed))

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
    """Move to frame is a call that moves the robot in cartesian space.
    The external axes (if any) will stay in the same position.

    Examples
    --------
    .. code-block:: python

        # Get frame
        frame = abb.send_and_wait(rrc.GetFrame())

        # Print received values
        print(frame)

        # Change any frame value and move robot to new position
        frame.point[0] += 50
        speed = 100 # Unit [mm/s]
        done = abb.send_and_wait(rrc.MoveToFrame(frame, speed, rrc.Zone.FINE, rrc.Motion.LINEAR))

    RAPID Instruction: ``MoveJ`` or ``MoveL``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, frame, speed, zone, motion_type=Motion.JOINT, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        frame : :class:`compas.geometry.Frame`
            Target frame.
        speed : :obj:`float`
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.
        zone : :class:`Zone`
            Zone data. Predefined in the robot controller,
            only Zone :attr:`Zone.FINE` will do a stop point all others are fly by points
        motion_type : :class:`Motion`
            Motion type. Defaults to :attr:`Motion.JOINT`.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
            Use  :attr:`FeedbackLevel.DONE` and :attr:`Zone.FINE` together to make sure
            the motion planner has executed the instruction fully.
        """
        super(MoveToFrame, self).__init__(frame, [], speed, zone, feedback_level)
        instruction = 'MoveTo'
        self.instruction = INSTRUCTION_PREFIX + instruction
        self.string_values = ['FrameJ'] if motion_type == Motion.JOINT else ['FrameL']


class MoveToRobtarget(MoveGeneric):
    """Move to robtarget is a call that moves the robot in cartesian space with explicit external axes values.

    Examples
    --------
    .. code-block:: python

        # Get frame and external axes
        frame, external_axes = abb.send_and_wait(rrc.GetRobtarget())

        # Print received values
        print(frame, external_axes)

        # Change any value and move to new position
        frame.point[0] += 50
        speed = 100 # Unit [mm/s]
        done = abb.send_and_wait(rrc.MoveToRobtarget(frame, external_axes, speed, rrc.Zone.FINE))

    RAPID Instruction: ``MoveJ`` or ``MoveL``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, frame, ext_axes, speed, zone, motion_type=Motion.JOINT, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        frame : :class:`compas.geometry.Frame`
            Target frame.
        ext_axes : :class:`compas_rrc.ExternalAxes` or :obj:`list` of :obj:`float`
            External axes positions.
        speed : :obj:`float`
            Integer specifying TCP translational speed in mm/s. Min=``0.01``.
        zone : :class:`Zone`
            Zone data. Predefined in the robot controller,
            only Zone :attr:`Zone.FINE` will do a stop point all others are fly by points
        motion_type : :class:`Motion`
            Motion type. Defaults to :attr:`Motion.JOINT`.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
            Use  :attr:`FeedbackLevel.DONE` and :attr:`Zone.FINE` together to make sure
            the motion planner has executed the instruction fully.
        """
        super(MoveToRobtarget, self).__init__(frame, ext_axes, speed, zone, feedback_level)
        instruction = 'MoveTo'
        self.instruction = INSTRUCTION_PREFIX + instruction
        self.string_values = ['J'] if motion_type == Motion.JOINT else ['L']
