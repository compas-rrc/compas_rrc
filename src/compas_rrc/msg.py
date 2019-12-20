from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'


class PrintText(ROSmsg):
    """Print text is a call that prints a text on the roboter panel (FlexPendant or TeachPendant).

    RAPID Instruction: TPWrite
    """

    def __init__(self, text, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'TPWrite'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [text]
        self.float_values = []
