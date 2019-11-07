from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

class WatchFeedback(object):
    """Represents valid feedback levels for project instructions."""
    NONE = 0
    DONE = 1

class WatchRead(ROSmsg):
    def __init__(self, feedback_level=WatchFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WatchRead'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):

        # read input value
        result = round(result['float_values'][0],3)
        return result

class WatchStart(ROSmsg):
    def __init__(self, feedback_level=WatchFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WatchStart'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

class WatchStop(ROSmsg):
    def __init__(self, feedback_level=WatchFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WatchStop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []
