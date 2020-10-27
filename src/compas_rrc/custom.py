from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

__all_ = ['CustomInstruction']


class CustomInstruction(ROSmsg):
    """Custom instruction is a call that calls a custom RAPID instruction. The name has to match to a ``RAPID`` procedure.

    Examples
    --------
    .. code-block:: python

        # Custom instruction
        string_values = ['Custom Text']
        float_values = [42]
        done = abb.send_and_wait(CustomInstruction('r_RRC_CustomInstruction', string_values, float_values))

    RAPID Instruction: ``All usable``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, name, string_values=[], float_values=[], feedback_level=FeedbackLevel.NONE, exec_level=ExecutionLevel.ROBOT):
        self.instruction = name
        self.feedback_level = feedback_level
        # self.exec_level = ExecutionLevel.ROBOT
        self.exec_level = exec_level
        self.string_values = string_values
        self.float_values = float_values
