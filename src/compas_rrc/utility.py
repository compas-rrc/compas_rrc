from compas.geometry import Frame
from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import ExternalAxes
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import RobotJoints

__all__ = ['Noop',
           'GetFrame',
           'GetJoints',
           'GetRobtarget']

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


class GetJoints(ROSmsg):
    """Get joints is a call that queries the axis values of the robot.

    RAPID Instruction: GetJointT
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetJointT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):
        # read robot jonts
        robot_joints = [result['float_values'][i] for i in range(18, 24)]

        # read external axes
        external_axes = [result['float_values'][i] for i in range(24, 27) if not is_rapid_none(result['float_values'][i])]

        # write result
        return RobotJoints(*robot_joints), ExternalAxes(*external_axes)


class GetRobtarget(ROSmsg):
    """Query the current robtarget (defined as frame + external axes) of the robot.

    RAPID Instruction: ``GetRobT``
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetRobT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):

        # read pos
        x = result['float_values'][17]
        y = result['float_values'][18]
        z = result['float_values'][19]
        pos = [x, y, z]

        # read orient
        orient_q1 = result['float_values'][20]
        orient_q2 = result['float_values'][21]
        orient_q3 = result['float_values'][22]
        orient_q4 = result['float_values'][23]
        orientation = [orient_q1, orient_q2, orient_q3, orient_q4]

        # read gantry joints
        external_axes = [result['float_values'][i] for i in range(24, 27) if not is_rapid_none(result['float_values'][i])]

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


class SetWobj(ROSmsg):
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
