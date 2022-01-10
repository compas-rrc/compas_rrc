import json

from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import SystemInstruction

__all__ = [
    'SystemStop',
    'SystemCustomInstruction',
]

class SystemStop(ROSmsg, SystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        self.instruction = 'stop'
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.DRIVER
        self.string_values = []
        self.float_values = []


class SystemCustomInstruction(ROSmsg, SystemInstruction):
    def __init__(self, name, method='GET', data=None, feedback_level=FeedbackLevel.DATA):
        if data is not None:
            method = 'POST'
        self.instruction = json.dumps(dict(path=name, method=method, data=data))
        self.feedback_level = feedback_level
        self.exec_level = ExecutionLevel.DRIVER
        self.string_values = []
        self.float_values = []

    def parse_feedback(self, response):
        return json.loads(response['feedback'])
