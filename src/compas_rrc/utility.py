from compas.geometry import Frame
from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import ExternalAxes
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import RobotJoints

__all__ = ['Noop',
           'GetJoints']

INSTRUCTION_PREFIX = 'r_A042_'


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
        external_axes = [result['float_values'][i] for i in range(24, 27) if not self.is_rapid_none(result['float_values'][i])]

        # write result
        return RobotJoints(*robot_joints), ExternalAxes(*external_axes)

    def is_rapid_none(self, val):
        """In RAPID, None values are expressed as 9E+9, they end up as 8999999488 in Python"""
        return int(val) == 8999999488


class GetFrame(ROSmsg):
    """Get frame is a call that queries the position of the robot in the cartisian space.

    RAPID Instruction: GetRobT
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetRobT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):

        # read pos
        self.pos_x = round(result['float_values'][17], 2)
        self.pos_y = round(result['float_values'][18], 2)
        self.pos_z = round(result['float_values'][19], 2)
        self.pos = [self.pos_x, self.pos_y, self.pos_z]

        # read orient
        self.orient_q1 = round(result['float_values'][20], 4)
        self.orient_q2 = round(result['float_values'][21], 4)
        self.orient_q3 = round(result['float_values'][22], 4)
        self.orient_q4 = round(result['float_values'][23], 4)
        self.orient = [self.orient_q1, self.orient_q2, self.orient_q3, self.orient_q4]

        # read gantry joints
        self.ext_axes_1 = round(result['float_values'][24], 2)
        self.ext_axes_2 = round(result['float_values'][25], 2)
        self.ext_axes_3 = round(result['float_values'][26], 2)
        self.ext_axes = [self.ext_axes_1, self.ext_axes_2, self.ext_axes_3]

        # write result

        # As compas frame
        result = Frame.from_quaternion([self.orient_q1, self.orient_q2, self.orient_q3, self.orient_q4], point=[self.pos_x, self.pos_y, self.pos_z])

        # As pos, orient and external axes values
        # result = [self.pos, self.orient, self.ext_axes]

        # End
        return result, ExternalAxes(*self.ext_axes)


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
