from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

class UtilityFeedback(object):
    """Represents valid feedback levels for project instructions."""
    NONE = 0
    DONE = 1

class Dummy(ROSmsg):
    def __init__(self, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'Dummy'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

class GetJointT(ROSmsg):
    def __init__(self, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetJointT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):

        # read robot jonts
        robot_joint_1 = round(result['float_values'][18],2)
        robot_joint_2 = round(result['float_values'][19],2)
        robot_joint_3 = round(result['float_values'][20],2)
        robot_joint_4 = round(result['float_values'][21],2)
        robot_joint_5 = round(result['float_values'][22],2)
        robot_joint_6 = round(result['float_values'][23],2)
        robot_joint = [robot_joint_1,robot_joint_2,robot_joint_3,robot_joint_4,robot_joint_5,robot_joint_6]

        # read gantry joints
        gantry_joint_x = round(result['float_values'][24],2)
        gantry_joint_y = round(result['float_values'][25],2)
        gantry_joint_z = round(result['float_values'][26],2)
        gantry_joint = [gantry_joint_x, gantry_joint_y, gantry_joint_z]

        # write result
        result = [robot_joint, gantry_joint]
        return result


class GetRobT(ROSmsg):
    def __init__(self, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'GetRobT'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

class SetAcc(ROSmsg):
    def __init__(self, acc, ramp, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetAcc'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [acc, ramp]

class SetTool(ROSmsg):
    def __init__(self, tool_name, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetTool'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [tool_name]
        self.float_values = []

class SetVel(ROSmsg):
    def __init__(self, override, max_tcp, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetVel'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [override, max_tcp]

class SetWobj(ROSmsg):
    def __init__(self, wobj_name, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetWobj'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [wobj_name]
        self.float_values = []

class Stop(ROSmsg):

    def __init__(self, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'Stop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

class WaitTime(ROSmsg):
    def __init__(self, time, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WaitTime'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = [time]
