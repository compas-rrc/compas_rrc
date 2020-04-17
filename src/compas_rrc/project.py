from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import ExecutionLevel


class CustomInstruction(ROSmsg):
    """Custom instruction is a call that calls a custom RAPID instruction. The name has to match to a ``RAPID`` procedure.


    RAPID Instruction: CustomInstruction
    """

    def __init__(self, name, string_values=[], float_values=[], feedback_level=FeedbackLevel.NONE, exec_level=ExecutionLevel.ROBOT):
        self.instruction = name
        self.feedback_level = feedback_level
        # self.exec_level = ExecutionLevel.ROBOT
        self.exec_level = exec_level
        self.string_values = string_values
        self.float_values = float_values
