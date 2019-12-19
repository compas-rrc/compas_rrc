from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

class SetDigital(ROSmsg):
    """Set Digital is a call that sets the value of an digital output signal (0 or 1).

    RAPID Instruction: SetDo
    """
    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetAnalog(ROSmsg):
    """Set Analog is a call that sets the value of an analog output signal (float).

    RAPID Instruction: SetAo
    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetAo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]


class SetGo(ROSmsg):
    """Set Group is a call that sets the value of an digital group output signal (Integer Value, depending on the size of the group ).

    RAPID Instruction: SetGo
    """

    def __init__(self, io_name, value, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetGo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [value]

class PulseDigital(ROSmsg):
    """Pulse Digital is a call that sets the value to high of an digital output signal for a certain time.

    RAPID Instruction: PulseDo
    """

    def __init__(self, io_name, pulse_time, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'PulseDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [pulse_time]

class ReadAnalog(ROSmsg):
    """Read Analog is a call that returns the value of an analog input signal.

    RAPID Instruction: ReadAi
    """

    def __init__(self, io_name, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadAi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = round(result['float_values'][0],2)
        return result

class ReadDigital(ROSmsg):
    """Read Digital is a call that returns the value of an digital input signal.

    RAPID Instruction: ReadDi
    """
    def __init__(self, io_name, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadDi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = int(result['float_values'][0])
        return result

class ReadGroup(ROSmsg):
    """Read Group is a call that returns the value of an digital group input signal.

    RAPID Instruction: ReadGi
    """
    def __init__(self, io_name, feedback_level=FeedbackLevel.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadGi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read input value
        result = int(result['float_values'][0])
        return result
