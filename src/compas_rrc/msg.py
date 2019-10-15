from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

class MsgFeedback(object):
    """Represents valid feedback levels for msg instructions."""
    NONE = 0
    DONE = 1

class TPWrite(ROSmsg):
    def __init__(self, text, feedback_level=MsgFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'TPWrite'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [text]
        self.float_values = []

