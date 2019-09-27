from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel

class ProjectFeedback(object):
    """Represents valid feedback levels for project instructions."""
    NONE = 0
    DONE = 1

class ProjectInstruction(ROSmsg):
    def __init__(self, name, string_values=[], float_values=[], feedback_level=ProjectFeedback.NONE):
        self.instruction = name
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = string_values
        self.float_values = float_values
