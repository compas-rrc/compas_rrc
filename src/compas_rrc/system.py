from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import SystemInstruction


__all__ = [
    'SystemStop',
]

class SystemStop(ROSmsg, SystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DONE):
        self.instruction = 'stop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.ROBOT
        self.string_values = []
        self.float_values = []
