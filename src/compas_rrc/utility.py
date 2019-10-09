from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

class UtilityFeedback(object):
    """Represents valid feedback levels for project instructions."""
    NONE = 0
    DONE = 1

class Stop(ROSmsg):

    def __init__(self, feedback_level=UtilityFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'Stop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []
