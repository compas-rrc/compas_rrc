from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import ExecutionLevel

INSTRUCTION_PREFIX = 'r_A042_'

class IOFeedback(object):
    """Represents valid feedback levels for project instructions."""
    NONE = 0
    DONE = 1


class SetDo(ROSmsg):

    def __init__(self, io_name, feedback_level=IOFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'SetDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = []


class ResetDo(ROSmsg):

    def __init__(self, io_name, feedback_level=IOFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'ResetDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = []


class PulseDo(ROSmsg):

    def __init__(self, io_name, pulse_time, feedback_level=IOFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'PulseDo'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]
        self.float_values = [pulse_time]

class ReadAi(ROSmsg):

    def __init__(self, io_name, feedback_level=IOFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadAi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read analog input value
        result = round(result['float_values'][0],2)
        return result

class ReadDi(ROSmsg):

    def __init__(self, io_name, feedback_level=IOFeedback.NONE):
        self.instruction = INSTRUCTION_PREFIX + 'ReadDi'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = [io_name]

    def parse_feedback(self, result):

        # read analog input value
        result = int(result['float_values'][0])
        return result

