from compas.geometry import Frame
from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import ExternalAxes
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import RobotJoints

__all__ = ['Noop',
           'GetFrame',
           'GetJoints',
           'GetRobtarget',
           'SetAcceleration',
           'SetTool',
           'SetMaxSpeed',
           'Stop',
           'WaitTime',
           'SetWorkObject',
           'Debug']

INSTRUCTION_PREFIX = 'r_A042_'


def is_rapid_none(val):
    """In RAPID, None values are expressed as 9E+9, they end up as 8999999488 in Python"""
    return int(val) == 8999999488


class Noop(ROSmsg):
    """No-op is a call without any effect.

    RAPID Instruction: Dummy
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'Dummy'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []


class Debug(ROSmsg):
    """Activate debug mode on any instruction by wrapping it.

    Examples
    --------
    >>> abb.send_and_wait(Debug(GetJoints()))
    """

    def __init__(self, instruction, debug_parser=None):
        self._instruction = instruction
        self.debug_parser = debug_parser

    @property
    def msg(self):
        return self._instruction.msg

    @property
    def instruction(self):
        return self._instruction.instruction

    @property
    def sequence_id(self):
        return self._instruction.sequence_id

    @sequence_id.setter
    def sequence_id(self, value):
        self._instruction.sequence_id = value

    @property
    def feedback_level(self):
        return self._instruction.feedback_level

    @feedback_level.setter
    def feedback_level(self, value):
        self._instruction.feedback_level = value

    @property
    def exec_level(self):
        return self._instruction.exec_level

    @property
    def string_values(self):
        return self._instruction.string_values

    @property
    def float_values(self):
        return self._instruction.float_values

    def parse_feedback(self, result):
        if self.debug_parser:
            return self.debug_parser(result)
        return result


class GetJoints(ROSmsg):
    """Get joints is a call that queries the axis values of the robot.

    RAPID Instruction: GetJointT
    """

    def __init__(self, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetJointT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):
        # read robot jonts
        robot_joints = [result['float_values'][i] for i in range(0, 6)]

        # read external axes
        external_axes = [result['float_values'][i] for i in range(6, 12) if not is_rapid_none(result['float_values'][i])]

        # write result
        return RobotJoints(*robot_joints), ExternalAxes(*external_axes)


class GetRobtarget(ROSmsg):
    """Query the current robtarget (defined as frame + external axes) of the robot.

    RAPID Instruction: ``GetRobT``
    """

    def __init__(self, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetRobT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):

        # read pos
        x = result['float_values'][0]
        y = result['float_values'][1]
        z = result['float_values'][2]
        pos = [x, y, z]

        # read orient
        orient_q1 = result['float_values'][3]
        orient_q2 = result['float_values'][4]
        orient_q3 = result['float_values'][5]
        orient_q4 = result['float_values'][6]
        orientation = [orient_q1, orient_q2, orient_q3, orient_q4]

        # read gantry joints
        external_axes = [result['float_values'][i] for i in range(7, 13) if not is_rapid_none(result['float_values'][i])]

        # write result

        # As compas frame
        result = Frame.from_quaternion(orientation, point=pos)

        # End
        return result, ExternalAxes(*external_axes)


class GetFrame(GetRobtarget):
    """Query the current frame of the robot.

    RAPID Instruction: ``GetRobT``
    """
    def parse_feedback(self, result):
        frame, _ext_axes = super(GetFrame, self).parse_feedback(result)
        return frame


class SetAcceleration(ROSmsg):
    """Set acceleration is a call that sets the acc- and deceleration from the robot.

    RAPID Instruction: SetAcc
    """

    def __init__(self, acc, ramp, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetAcc'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [acc, ramp]


class SetTool(ROSmsg):
    """Set tool is a call that sets a pre defined tool in the robot as active.

    RAPID Instruction: SetTool
    """

    def __init__(self, tool_name, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetTool'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [tool_name]
        self.float_values = []


class SetMaxSpeed(ROSmsg):
    """Set max spedd is a call that limits the maximum TCP speed.

    RAPID Instruction: SetVel
    """

    def __init__(self, override, max_tcp, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetVel'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [override, max_tcp]


class SetWorkObject(ROSmsg):
    """Set work object is a call that sets a pre defined work object in the robot as active.

    RAPID Instruction: SetWobj
    """

    def __init__(self, wobj_name, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetWobj'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [wobj_name]
        self.float_values = []


class Stop(ROSmsg):
    """Stop is a call that stops the motion task from the robot.

    RAPID Instruction: Stop
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'Stop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []


class WaitTime(ROSmsg):
    """Wait time is a call that calls a wait instruction on the robot.

    RAPID Instruction: WaitTime
    """

    def __init__(self, time, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WaitTime'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [time]
