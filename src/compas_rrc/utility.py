from compas.geometry import Frame
from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.client import default_feedback_parser
from compas_rrc.common import BaseInstruction
from compas_rrc.common import ExecutionLevel
from compas_rrc.common import ExternalAxes
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import InstructionException
from compas_rrc.common import Interfaces
from compas_rrc.common import RobotJoints

INSTRUCTION_PREFIX = "r_RRC_"

__all__ = [
    "Debug",
    "GetFrame",
    "GetJoints",
    "GetRobtarget",
    "GetVariable",
    "Noop",
    "ResetApp",
    "SetAcceleration",
    "SetMaxSpeed",
    "SetTool",
    "SetWorkObject",
    "StartApp",
    "Stop",
    "StopApp",
    "WaitTime",
]


def is_rapid_none(val):
    """In RAPID, None values are expressed as 9E+9, they end up as 8999999488 in Python"""
    return int(val) == 8999999488


class Noop(BaseInstruction):
    """No-op is a call without any effect. But like all other instructions it makes a roundtrip from the user code to the robot and back.

    Examples
    --------
    .. code-block:: python

        # Noop
        done = abb.send_and_wait(rrc.Noop())

    RAPID Instruction: ``none``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(Noop, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "Noop"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []


class Debug(ROSmsg):
    """Activate debug mode on any instruction by wrapping it.

    Examples
    --------
    .. code-block:: python

        # Get joints
        raw_debug_output = abb.send_and_wait(rrc.Debug(rrc.GetJoints()))

        # Print received values
        print(raw_debug_output)

    """

    def __init__(self, instruction, debug_parser=None):
        """Initialize a new debug instruction wrapping another instruction.

        Parameters
        ----------
        instruction : :class:`ROSmsg`
            Any instruction inheriting from ROS message.
        debug_parser : callable
            Function to be used for parsing the feedback. Optional.
        """
        self._instruction = instruction
        self.debug_parser = debug_parser

    @property
    def msg(self):
        """Raw message."""
        return self._instruction.msg

    @property
    def instruction(self):
        """Name of the instruction."""
        return self._instruction.instruction

    @property
    def sequence_id(self):
        """Sequence identifier."""
        return self._instruction.sequence_id

    @sequence_id.setter
    def sequence_id(self, value):
        self._instruction.sequence_id = value

    @property
    def feedback_level(self):
        """Feedback level."""
        return self._instruction.feedback_level

    @feedback_level.setter
    def feedback_level(self, value):
        self._instruction.feedback_level = value

    @property
    def exec_level(self):
        """Execution level."""
        return self._instruction.exec_level

    @property
    def string_values(self):
        """List of string values."""
        return self._instruction.string_values

    @property
    def float_values(self):
        """List of float values."""
        return self._instruction.float_values

    def parse_feedback(self, result):
        if self.debug_parser:
            return self.debug_parser(result)
        return result


class GetJoints(BaseInstruction):
    """Get joints is a call that requests the joint values (:class:`RobotJoints`) and the external axes (:class:`ExternalAxes`) of the robot.

    Examples
    --------
    .. code-block:: python

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(rrc.GetJoints())

    RAPID Instruction: ``CJointT``

    .. include:: ../abb-reference.rst

    """

    def __init__(self):
        """Create a new instance of the instruction."""
        super(GetJoints, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "GetJoints"})
        self.feedback_level = FeedbackLevel.DONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):
        """Parses the result as :class:`RobotJoints` and :class:`ExternalAxes`.

        Return
        ------
        :class:`RobotJoints`, :class:`ExternalAxes`
            Current joints and external axes of the robot.
        """
        # read robot joints
        robot_joints = [result["float_values"][i] for i in range(0, 6)]

        # read external axes
        external_axes = [
            result["float_values"][i] for i in range(6, 12) if not is_rapid_none(result["float_values"][i])
        ]

        # write result
        return RobotJoints(*robot_joints), ExternalAxes(*external_axes)


class GetRobtarget(BaseInstruction):
    """Instruction to request the current robtarget defined as frame (:class:`compas.geometry.Frame`)
    and external axes (:class:`ExternalAxes`) of the robot.

    Examples
    --------
    .. code-block:: python

        # Get frame and external axes
        frame, external_axes = abb.send_and_wait(rrc.GetRobtarget())

    RAPID Instruction: ``CRobT``

    .. include:: ../abb-reference.rst

    """

    def __init__(self):
        """Create a new instance of the instruction."""
        super(GetRobtarget, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "GetRobtarget"})
        self.feedback_level = FeedbackLevel.DONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):
        """Parses the result as a :class:`compas.geometry.Frame` and :class:`ExternalAxes`.

        Return
        ------
        :class:`compas.geometry.Frame`, :class:`ExternalAxes`
            Current frame and external axes of the robot.
        """

        # read pos
        x = result["float_values"][0]
        y = result["float_values"][1]
        z = result["float_values"][2]
        pos = [x, y, z]

        # read orient
        orient_q1 = result["float_values"][3]
        orient_q2 = result["float_values"][4]
        orient_q3 = result["float_values"][5]
        orient_q4 = result["float_values"][6]
        orientation = [orient_q1, orient_q2, orient_q3, orient_q4]

        # read gantry joints
        external_axes = [
            result["float_values"][i] for i in range(7, 13) if not is_rapid_none(result["float_values"][i])
        ]

        # write result

        # As compas frame
        result = Frame.from_quaternion(orientation, point=pos)

        # End
        return result, ExternalAxes(*external_axes)


class GetFrame(GetRobtarget):
    """Instruction to request the current frame (:class:`compas.geometry.Frame`) of the robot.

    Examples
    --------
    .. code-block:: python

        # Get frame
        frame = abb.send_and_wait(rrc.GetFrame())

    RAPID Instruction: ``CRobT``

    .. include:: ../abb-reference.rst

    """

    def parse_feedback(self, result):
        """Parses the result as a :class:`compas.geometry.Frame`.

        Return
        ------
        :class:`compas.geometry.Frame`
            Current frame of the robot.
        """
        frame, _ext_axes = super(GetFrame, self).parse_feedback(result)
        return frame


class SetAcceleration(BaseInstruction):
    """Set acceleration is a call that sets the acc- and deceleration of the robot.

    Examples
    --------
    .. code-block:: python

        # Set acceleration
        acc = 100 # Unit [%]
        ramp = 100  # Unit [%]
        done = abb.send_and_wait(rrc.SetAcceleration(acc, ramp))

    RAPID Instruction: ``AccSet``

    .. include:: ../abb-reference.rst
    """

    def __init__(self, acc, ramp, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        acc : :obj:`float`
            Acceleration or deceleration expressed in percentage of the system parameters of the robot.
        ramp : :obj:`float`
            The rate at which acceleration or deceleration changes expressed in percentage.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(SetAcceleration, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "SetAcceleration"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [acc, ramp]


class SetTool(BaseInstruction):
    """Set tool is a call that sets a predefined tool in the robot as active.

    Examples
    --------
    .. code-block:: python

        # Set tool
        done = abb.send_and_wait(rrc.SetTool('tool0'))

    RAPID Instruction: ``tooldata``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, tool_name, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        tool_name : :obj:`str`
            Name of the tool as defined in RAPID.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(SetTool, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "SetTool"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [tool_name]
        self.float_values = []


class SetMaxSpeed(BaseInstruction):
    """Set max speed is a call that sets the override and maximal tool center point (TCP) speed from the robot.

    Examples
    --------
    .. code-block:: python

        # Set max speed
        override = 100 # Unit [%]
        max_tcp = 2500 # Unit [mm/s]
        done = abb.send_and_wait(rrc.SetMaxSpeed(override, max_tcp))

    RAPID Instruction: ``VelSet``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, override, max_tcp, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        override : :obj:`float`
            Internal speed override expressed in percentage. This override is additional to the one that
            can be defined on the robot panel. It is recommended to use only one of them, preferably the
            one on the robot panel, and leave this to 100%.
        max_tcp : :obj:`float`
            Maximum tool center point (TCP) speed expressed in mm/sec. All instructions following a ``SetMaxSpeed``
            are affected by it.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(SetMaxSpeed, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "SetMaxSpeed"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [override, max_tcp]


class SetWorkObject(BaseInstruction):
    """Set work object is a call that sets a predefined work object in the robot as active.

    Examples
    --------
    .. code-block:: python

        # Set work object
        done = abb.send_and_wait(rrc.SetWorkObject('wobj0'))

    RAPID Instruction: ``wobjdata``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, wobj_name, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        wobj_name : :obj:`str`
            Name of the work object as defined in RAPID.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(SetWorkObject, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "SetWorkObject"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [wobj_name]
        self.float_values = []


class Stop(BaseInstruction):
    """Stop is a function to stop the associated motion task of the robot.

    Examples
    --------
    .. code-block:: python

        # Stop
        done = abb.send_and_wait(rrc.Stop())

    RAPID Instruction: ``Stop``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(Stop, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "Stop"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []


class WaitTime(BaseInstruction):
    """Wait time is a call that will wait on the robot task for a certain time.

    Examples
    --------
    .. code-block:: python

        # Wait time
        time = 1.0 # Unit [s]
        done = abb.send_and_wait(rrc.WaitTime(time))

    RAPID Instruction: ``WaitTime``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, time, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        time : :obj:`float`
            Duration of the wait expressed in seconds.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(WaitTime, self).__init__({Interfaces.APP: INSTRUCTION_PREFIX + "WaitTime"})
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [time]


class StartApp(BaseInstruction):
    """Start the application-level code on the robot controller.

    Examples
    --------
    .. code-block:: python

        # Start app
        done = abb.send_and_wait(rrc.StartApp())

    """

    def __init__(self, feedback_level=FeedbackLevel.DATA):
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.DATA`.
        """
        super(StartApp, self).__init__({Interfaces.SYS: "start"}, default_interface=Interfaces.SYS)
        self.feedback_level = feedback_level


class StopApp(BaseInstruction):
    """Stop the application-level code on the robot controller.

    Examples
    --------
    .. code-block:: python

        # Start app
        done = abb.send_and_wait(rrc.StopApp())

    """

    def __init__(self, feedback_level=FeedbackLevel.DATA):
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.DATA`.
        """
        super(StopApp, self).__init__({Interfaces.SYS: "stop"}, default_interface=Interfaces.SYS)
        self.feedback_level = feedback_level


class ResetApp(BaseInstruction):
    """Reset the application-level code on the robot controller.

    In ABB robots, this is equivalent to reseting the program pointer
    to main (ie. ``PP to Main``).

    Examples
    --------
    .. code-block:: python

        # Start app
        done = abb.send_and_wait(rrc.ResetApp())

    """

    def __init__(self, feedback_level=FeedbackLevel.DATA):
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.DATA`.
        """
        super(ResetApp, self).__init__({Interfaces.SYS: "reset_program_pointer"}, default_interface=Interfaces.SYS)
        self.feedback_level = feedback_level


class GetVariable(BaseInstruction):
    """Get the value of a variable defined in robot code.

    Examples
    --------
    .. code-block:: python

        # Start app
        result = abb.send_and_wait(rrc.GetVariable("t_RRC_ActTool", "T_ROB1"))
        print("Tool = ", result)

    """

    def __init__(self, variable_name, task_name, feedback_level=FeedbackLevel.DATA):
        """Create a new instance of the instruction.

        Parameters
        ----------
        variable_name : :obj:`str`
            Variable name to retrieve.
        task_name : :obj:`str`
            Robot task in which the variable is to be found, e.g. ``T_ROB1``.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.DATA`.
        """
        super(GetVariable, self).__init__({Interfaces.SYS: "get_variable"}, default_interface=Interfaces.SYS)
        self.feedback_level = feedback_level
        self.string_values = [variable_name, task_name]
        self.float_values = []

    def parse_feedback(self, result):
        """Parses the value of the variable.

        Return
        ------
        obj
            Value of the variable (the type depends on its type on the robot program).
        """
        # Make sure the default parsers take care of turning basic error messages
        # into exceptions. In that case, return it (the raising of that is handled by FutureResult)
        feedback_value = default_feedback_parser(result)
        if isinstance(feedback_value, Exception):
            return feedback_value

        if not len(result["string_values"]):
            return None

        if len(result["string_values"]) > 2:
            raise InstructionException(
                "Unexpected return value. Expected 2 string values, got {}.".format(len(result["string_values"])),
                result,
            )

        raw_value = result["string_values"][0]
        type_name = result["string_values"][1]

        value = self.client.parse_variable_value(raw_value, type_name)
        return value
