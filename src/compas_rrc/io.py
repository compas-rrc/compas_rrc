from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

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

    RAPID Instruction: SetDo
    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        if value not in (0, 1):
            raise ValueError("Value can only be 0 or 1")
        self.instruction = INSTRUCTION_PREFIX + 'SetDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetAnalog(ROSmsg):
    """Set analog is a call that sets the value of an analog output signal (float).

    RAPID Instruction: SetAo
    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetAo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetGroup(ROSmsg):
    """Set group is a call that sets the value of an digital group output signal (Integer Value, depending on the size of the group ).

    RAPID Instruction: SetGo
    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetGo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class PulseDigital(ROSmsg):
    """Pulse digital is a call that sets the value to high of an digital output signal for a certain time.

    RAPID Instruction: PulseDo
    """

    def __init__(self, io_name, pulse_time, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'PulseDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [pulse_time]


class ReadAnalog(ROSmsg):
    """Read analog is a call that returns the value of an analog input signal.

    RAPID Instruction: ReadAi
    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadAi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):
        # read input value
        result = result['float_values'][0]
        return result


class ReadDigital(ROSmsg):
    """Read digital is a call that returns the value of an digital input signal.

    RAPID Instruction: ReadDi
    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadDi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = int(result['float_values'][0])
        return result


class ReadGroup(ROSmsg):
    """Read group is a call that returns the value of an digital group input signal.

    RAPID Instruction: ReadGi
    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.DONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadGi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = int(result['float_values'][0])
        return result
