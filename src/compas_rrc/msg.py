from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

INSTRUCTION_PREFIX = 'r_RRC_'

__all__ = [
    'PrintText'
]


class PrintText(ROSmsg):
    """Print text is a call that prints a text on the roboter panel.

    Examples
    --------
    .. code-block:: python

        # Print text
        done = abb.send_and_wait(PrintText('Welcome to COMPAS_RRC'))

    RAPID Instruction: ``TPWrite``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, text, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'PrintText'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [text]
        self.float_values = []
