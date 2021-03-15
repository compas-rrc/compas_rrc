from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

__all__ = ['CustomInstruction']


class CustomInstruction(ROSmsg):
    """Custom instruction is a call that invokes a custom RAPID instruction. The name has to match a ``RAPID`` procedure.

    Examples
    --------
    .. code-block:: python

        # Custom instruction
        string_values = ['Custom Text']
        float_values = [42]
        done = abb.send_and_wait(rrc.CustomInstruction('r_RRC_CustomInstruction', string_values, float_values))

    RAPID Instruction: ``All usable``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, name, string_values=[], float_values=[], feedback_level=FeedbackLevel.NONE, execution_level=ExecutionLevel.ROBOT):
        """Create a new instance of the instruction.

        Parameters
        ----------
        name : :obj:`str`
            Name of the procedure to invoke on the robot code. Maximum of 80 characters.
        string_values : :obj:`list` of :obj:`str`
            List of up to 8 strings values, each of them with a maximum of 80 characters.
        float_values : :obj:`list` of :obj:`float`
            List of up to 36 float values.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        execution_level : :obj:`int`
            Defines the execution level of the instruction. Defaults to :attr:`ExecutionLevel.ROBOT`.
        """
        self.instruction = name
        self.feedback_level = feedback_level
        self.exec_level = execution_level
        self.string_values = string_values
        self.float_values = float_values
