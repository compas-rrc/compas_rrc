from compas_fab.backends.ros.messages import ROSmsg


class ProjectInstruction(ROSmsg):
    def __init__(self, name, string_values=[], float_values=[], feedback_level=MotionFeedback.NONE):
        self.instruction = name
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = string_values
        self.float_values = float_values
