from compas_fab.backends.ros.messages import ROSmsg
from compas_rrc.common import ExecutionLevel

class ProjectFeedback(object):
    """Represents valid feedback levels for project instructions."""
    NONE = 0
    DONE = 1

class ProjectInstruction(ROSmsg):
    """Represents a non-standard, project-specific instructions.

    The name has to match to a ``RAPID`` procedure, which will be called once
    the message arrives to the controller."""
    def __init__(self, name, string_values=[], float_values=[], feedback_level=ProjectFeedback.NONE):
        self.instruction = name
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = string_values
        self.float_values = float_values
