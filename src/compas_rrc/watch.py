from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

INSTRUCTION_PREFIX = 'r_RRC_'

__all__ = [
    'INSTRUCTION_PREFIX',
    'ReadWatch',
    'StartWatch',
    'StopWatch',
]


class ReadWatch(ROSmsg):
    """Read Watch is a call that returns the value from the watch in the robot code.

    Examples
    --------
    .. code-block:: python

        # Read watch
        watch_time = abb.send_and_wait(ReadWatch())

    RAPID Instruction: ``ClkRead``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadWatch'
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

    Examples
    --------
    .. code-block:: python

        # Start watch
        done = abb.send_and_wait(StartWatch())

    RAPID Instruction: ``ClkStart``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'StartWatch'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []


class StopWatch(ROSmsg):
    """Stop Watch is a call that stops the watch in the robot code.

    Examples
    --------
    .. code-block:: python

        # Stop watch
        done = abb.send_and_wait(StopWatch())

    RAPID Instruction: ``ClkStop``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'StopWatch'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []
