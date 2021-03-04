from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

INSTRUCTION_PREFIX = 'r_RRC_'

__all__ = [
    'PrintText'
]


class PrintText(ROSmsg):
    """Print text is a call that prints a single line of text on the robot panel.

    Examples
    --------
    .. code-block:: python

        # Print text
        done = abb.send_and_wait(rrc.PrintText('Welcome to COMPAS_RRC'))

    RAPID Instruction: ``TPWrite``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, text, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        text : :obj:`str`
            Single line of text to print on the robot panel with a maximum of 80 characters.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        if len(text) > 80:
            raise ValueError("text can only be up to 80 chars")
        self.instruction = INSTRUCTION_PREFIX + 'PrintText'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [text]
        self.float_values = []
