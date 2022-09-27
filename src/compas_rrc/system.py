import json

from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import SystemInstruction

__all__ = [
    'GetControllerState',
    'GetSpeedRatio',
    'GetTaskExecutionState',
    'GetTasks',
    'SystemCustomInstruction',
    'SystemGetDigital',
    'SystemSetDigital',
    'SystemGetAnalog',
    'SystemSetAnalog',
    'SystemStart',
    'SystemStop',
]


class BaseSystemInstruction(ROSmsg, SystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA, execution_level=ExecutionLevel.DRIVER):
        super(BaseSystemInstruction, self).__init__()
        self.feedback_level = feedback_level
        self.exec_level = execution_level
        self.string_values = []
        self.float_values = []


class SystemCustomInstruction(BaseSystemInstruction):
    def __init__(self, name, method='GET', data=None, feedback_level=FeedbackLevel.DATA):
        super(SystemCustomInstruction, self).__init__(feedback_level)
        if data is not None:
            method = 'POST'
        self.instruction = json.dumps(dict(path=name, method=method, data=data))

    def parse_feedback(self, response):
        return json.loads(response['feedback'])


class SystemStart(BaseSystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(SystemStart, self).__init__(feedback_level)
        self.instruction = 'start'


class SystemStop(BaseSystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(SystemStop, self).__init__(feedback_level)
        self.instruction = 'stop'


class SystemSetDigital(BaseSystemInstruction):
    def __init__(self, signal_name, signal_value, feedback_level=FeedbackLevel.DATA):
        super(SystemSetDigital, self).__init__(feedback_level)
        if signal_value not in (0, 1):
            raise ValueError('Signal value must be 0 or 1')

        self.instruction = 'set_signal'
        self.string_values = [signal_name]
        self.float_values = [signal_value]


class SystemGetDigital(BaseSystemInstruction):
    def __init__(self, signal_name, feedback_level=FeedbackLevel.DATA):
        super(SystemGetDigital, self).__init__(feedback_level)
        self.instruction = 'get_signal'
        self.string_values = [signal_name]

    def parse_feedback(self, response):
        return int(response['float_values'][0])


class SystemSetAnalog(BaseSystemInstruction):
    def __init__(self, signal_name, signal_value, feedback_level=FeedbackLevel.DATA):
        super(SystemSetAnalog, self).__init__(feedback_level)
        self.instruction = 'set_signal'
        self.string_values = [signal_name]
        self.float_values = [signal_value]


class SystemGetAnalog(BaseSystemInstruction):
    def __init__(self, signal_name, feedback_level=FeedbackLevel.DATA):
        super(SystemGetAnalog, self).__init__(feedback_level)
        self.instruction = 'get_signal'
        self.string_values = [signal_name]

    def parse_feedback(self, response):
        return response['float_values'][0]


class SystemSetGroup(BaseSystemInstruction):
    def __init__(self, signal_name, signal_value, feedback_level=FeedbackLevel.DATA):
        super(SystemSetGroup, self).__init__(feedback_level)
        self.instruction = 'set_signal'
        self.string_values = [signal_name]
        self.float_values = [signal_value]


class SystemGetGroup(BaseSystemInstruction):
    def __init__(self, signal_name, feedback_level=FeedbackLevel.DATA):
        super(SystemGetGroup, self).__init__(feedback_level)
        self.instruction = 'get_signal'
        self.string_values = [signal_name]

    def parse_feedback(self, response):
        return int(response['float_values'][0])


class GetControllerState(BaseSystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetControllerState, self).__init__(feedback_level)
        self.instruction = 'get_controller_state'

    def parse_feedback(self, response):
        return response['string_values'][0]


class GetSpeedRatio(BaseSystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetSpeedRatio, self).__init__(feedback_level)
        self.instruction = 'get_speed_ratio'

    def parse_feedback(self, response):
        return response['float_values'][0]


class GetTasks(BaseSystemInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetTasks, self).__init__(feedback_level)
        self.instruction = 'get_tasks'

    def parse_feedback(self, response):
        return json.loads(response['feedback'])


class GetTaskExecutionState(BaseSystemInstruction):
    def __init__(self, task_name, feedback_level=FeedbackLevel.DATA):
        super(GetTaskExecutionState, self).__init__(feedback_level)
        self.instruction = 'get_task_execution_state'
        self.string_values = [task_name]

    def parse_feedback(self, response):
        return response['string_values'][0]
