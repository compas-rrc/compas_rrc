from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'


class ReadWatch(ROSmsg):
    """Read Watch is a call that returns the value from the watch in the robot code.

    RAPID Instruction: WatchRead
    """

    def __init__(self, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'WatchRead'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, result):

        # read input value
        result = round(result['float_values'][0], 3)
        return result


class StartWatch(ROSmsg):
    """Start Watch is a call that starts the watch in the robot code.

    RAPID Instruction: WatchStart
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WatchStart'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []


class StopWatch(ROSmsg):
    """Stop Watch is a call that stops the watch in the robot code.

    RAPID Instruction: WatchStop
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'WatchStop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []
