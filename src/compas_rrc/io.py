from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

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


class SetDigital(ROSmsg):
    """Set digital is a call that sets the value of an digital output signal (0 or 1).

    Examples
    --------
    .. code-block:: python

        # Set digital output to low or high
        low = 0
        high = 1
        done = abb.send_and_wait(SetDigital('do_1',low))

    RAPID Instruction: ``SetDO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        if value not in (0, 1):
            raise ValueError("Value can only be 0 or 1")
        self.instruction = INSTRUCTION_PREFIX + 'SetDigital'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetAnalog(ROSmsg):
    """Set analog is a call that sets the value of an analog output signal (float). Minimum and maximum values are given by the signal configuration in the robot.

    Examples
    --------
    .. code-block:: python

        # Set analog output
        value = -3.33
        done = abb.send_and_wait(SetAnalog('ao_1', value))

    RAPID Instruction: ``SetAO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetAnalog'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetGroup(ROSmsg):
    """Set group is a call that sets the value of an digital group output signal (Integer Value, depending on the size of the group ).

    Examples
    --------
    .. code-block:: python

        # Set group output
        value = 33
        done = abb.send_and_wait(SetGroup('go_1', value))

    RAPID Instruction: ``SetGO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetGroup'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class PulseDigital(ROSmsg):
    """Pulse digital is a call that sets the value to high of an digital output signal for a certain time.

    Examples
    --------
    .. code-block:: python

        # Pulse digital output
        pulse_time = 2.5 # Unit [s]
        done = abb.send_and_wait(PulseDigital('do_1', pulse_time))

    RAPID Instruction: ``PulseDO``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, pulse_time, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'PulseDigital'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [pulse_time]


class ReadAnalog(ROSmsg):
    """Read analog is a call that returns the value of an analog input signal.


    Examples
    --------
    .. code-block:: python

        # Read analog
        analog_input_1 = abb.send_and_wait(ReadAnalog('ai_1'))

    RAPID Instruction: ``AInput``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadAnalog'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):
        # read input value
        result = result['float_values'][0]
        return result


class ReadDigital(ROSmsg):
    """Read digital is a call that returns the value of an digital input signal.

    Examples
    --------
    .. code-block:: python

        # Read digital
        digital_input_1 = abb.send_and_wait(ReadDigital('di_1'))

    RAPID Instruction: ``DInput``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadDigital'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = int(result['float_values'][0])
        return result


class ReadGroup(ROSmsg):
    """Read group is a call that returns the value of an digital group input signal.

    Examples
    --------
    .. code-block:: python

        # Read group
        group_input_1 = abb.send_and_wait(ReadGroup('gi_1'))

    RAPID Instruction: ``GInput``

    .. include:: ../abb-reference.rst

    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadGroup'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = int(result['float_values'][0])
        return result
