from typing import Any
from typing import Dict
from typing import List
from typing import Union

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel
from compas_rrc.message import Instruction

INSTRUCTION_PREFIX = "r_RRC_"

__all__ = [
    "ReadWatch",
    "StartWatch",
    "StopWatch",
]


class ReadWatch(Instruction):
    """Read Watch is a call that requests the value of the watch in the robot code.

    Examples
    --------
    .. code-block:: python

        # Read watch
        watch_time = abb.send_and_wait(rrc.ReadWatch())  # Unit [s]

    RAPID Instruction: ``ClkRead``

    .. include:: ../abb-reference.rst

    """

    def __init__(self) -> None:
        """Create a new instance of the instruction."""
        self.instruction = INSTRUCTION_PREFIX + "ReadWatch"
        self.feedback_level = FeedbackLevel.DONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values: List[str] = []
        self.float_values: List[float] = []

    def parse_feedback(self, result: Union[Dict[str, Any], Any]) -> float:
        """Parses the result as a :obj:`float` (seconds).

        Return
        ------
        :obj:`float`
            Current value of the watch in seconds.
        """
        # read input value
        result = round(result["float_values"][0], 3)
        return result


class StartWatch(Instruction):
    """Start Watch is a call that starts the watch in the robot code.

    Examples
    --------
    .. code-block:: python

        # Start watch
        done = abb.send_and_wait(rrc.StartWatch())

    RAPID Instruction: ``ClkStart``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level: int = FeedbackLevel.NONE) -> None:
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        self.instruction = INSTRUCTION_PREFIX + "StartWatch"
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values: List[str] = []
        self.float_values: List[float] = []


class StopWatch(Instruction):
    """Stop Watch is a call that stops the watch in the robot code.

    Examples
    --------
    .. code-block:: python

        # Stop watch
        done = abb.send_and_wait(rrc.StopWatch())

    RAPID Instruction: ``ClkStop``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, feedback_level: int = FeedbackLevel.NONE) -> None:
        """Create a new instance of the instruction.

        Parameters
        ----------
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        self.instruction = INSTRUCTION_PREFIX + "StopWatch"
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values: List[str] = []
        self.float_values: List[float] = []
