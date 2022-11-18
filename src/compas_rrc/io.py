from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import BaseInstruction
from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import Interfaces

INSTRUCTION_PREFIX = 'r_RRC_'

__all__ = [
    'SetDigital',
    'SetAnalog',
    'SetGroup',
    'PulseDigital',
    'ReadAnalog',
    'ReadDigital',
    'ReadGroup',
]


class SetDigital(BaseInstruction):
    """Set digital is a call that sets the value of an digital output signal (:obj:`int`, 0 or 1).

    Examples
    --------
    .. code-block:: python

        # Set digital output to low or high
        low = 0
        high = 1
        done = abb.send_and_wait(rrc.SetDigital('do_1',low))

    RAPID Instruction: ``SetDO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the output signal.
        value : :obj:`int`
            Value of the output signal.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        if value not in (0, 1):
            raise ValueError("Value can only be 0 or 1")
        super(SetDigital, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'SetDigital',
            Interfaces.SYS: "set_signal"
        })

        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetAnalog(BaseInstruction):
    """Set analog is a call that sets the value of an analog output signal (:obj:`float`).
    Minimum and maximum values are given by the signal configuration in the robot.

    Examples
    --------
    .. code-block:: python

        # Set analog output
        value = -3.33
        done = abb.send_and_wait(rrc.SetAnalog('ao_1', value))

    RAPID Instruction: ``SetAO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the output signal.
        value : :obj:`float`
            Value of the output signal.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(SetAnalog, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'SetAnalog',
            Interfaces.SYS: "set_signal"
        })
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetGroup(BaseInstruction):
    """Set group is a call that sets the value of an digital group output signal (:obj:`int`).
    Minimum and maximum values are given by the signal configuration in the robot.

    Examples
    --------
    .. code-block:: python

        # Set group output
        value = 33
        done = abb.send_and_wait(rrc.SetGroup('go_1', value))

    RAPID Instruction: ``SetGO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the output signal.
        value : :obj:`int`
            Value of the output signal.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(SetGroup, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'SetGroup',
            Interfaces.SYS: "set_signal"
        })

        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class PulseDigital(BaseInstruction):
    """Pulse digital is a call that sets the value to HIGH of an digital output signal for a certain time.

    Examples
    --------
    .. code-block:: python

        # Pulse digital output
        pulse_time = 2.5 # Unit [s]
        done = abb.send_and_wait(rrc.PulseDigital('do_1', pulse_time))

    RAPID Instruction: ``PulseDO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, pulse_time, feedback_level=FeedbackLevel.NONE):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the output signal.
        pulse_time : :obj:`float`
            Duration of the pulse expressed in seconds.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        """
        super(PulseDigital, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'PulseDigital'
        })

        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [pulse_time]


class ReadAnalog(BaseInstruction):
    """Read analog is a call that requests the value of an analog input signal.

    Examples
    --------
    .. code-block:: python

        # Read analog
        analog_input_1 = abb.send_and_wait(rrc.ReadAnalog('ai_1'))

    RAPID Instruction: ``AInput``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the input signal.
        """
        super(ReadAnalog, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'ReadAnalog',
            Interfaces.SYS: "get_signal"
        })

        self.feedback_level = FeedbackLevel.DONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):
        """Parses the result as a :obj:`float`.

        Return
        ------
        :obj:`float`
            Current value of the input signal.
        """
        # read input value
        result = result['float_values'][0]
        return result


class ReadDigital(BaseInstruction):
    """Read digital is a call that requests the value of a digital input signal.

    Examples
    --------
    .. code-block:: python

        # Read digital
        digital_input_1 = abb.send_and_wait(rrc.ReadDigital('di_1'))

    RAPID Instruction: ``DInput``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the input signal.
        """
        super(ReadDigital, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'ReadDigital',
            Interfaces.SYS: "get_signal"
        })

        self.feedback_level = FeedbackLevel.DONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):
        """Parses the result as a :obj:`int`.

        Return
        ------
        :obj:`int`
            Current value of the input signal.
        """

        # read input value
        result = int(result['float_values'][0])
        return result


class ReadGroup(BaseInstruction):
    """Read group is a call that requests the value of a digital group input signal.

    Examples
    --------
    .. code-block:: python

        # Read group
        group_input_1 = abb.send_and_wait(rrc.ReadGroup('gi_1'))

    RAPID Instruction: ``GInput``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name):
        """Create a new instance of the instruction.

        Parameters
        ----------
        io_name : :obj:`str`
            Name of the input signal.
        """
        super(ReadGroup, self).__init__({
            Interfaces.APP: INSTRUCTION_PREFIX + 'ReadGroup',
            Interfaces.SYS: "get_signal"
        })

        self.feedback_level = FeedbackLevel.DONE
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):
        """Parses the result as a :obj:`int`.

        Return
        ------
        :obj:`int`
            Current value of the input signal.
        """

        # read input value
        result = int(result['float_values'][0])
        return result
