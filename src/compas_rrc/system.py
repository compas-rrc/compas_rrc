from compas_rrc.common import Interfaces
from compas_rrc.common import FeedbackLevel
from compas_rrc.common import BaseInstruction

__all__ = [
    "GetControllerState",
    "GetExecutionState",
    "GetOperationMode",
    "GetSpeedRatio",
    "SetSpeedRatio",
    # 'GetTaskExecutionState',
    # 'GetTasks',
    # 'SystemCustomInstruction',
    # 'SystemGetVariable',
    # 'SystemSetVariable',
    # 'SystemStart',
    # 'SystemStop',
]


class GetSpeedRatio(BaseInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetSpeedRatio, self).__init__({Interfaces.SYS: "get_speed_ratio"}, default_interface=Interfaces.SYS)
        self.feedback_level = feedback_level
        self.string_values = []
        self.float_values = []

    def on_after_receive(self, result, **kwargs):
        return int(result["float_values"][0])


class SetSpeedRatio(BaseInstruction):
    def __init__(self, speed_ratio, feedback_level=FeedbackLevel.DATA):
        super(SetSpeedRatio, self).__init__({Interfaces.SYS: "set_speed_ratio"}, default_interface=Interfaces.SYS)
        if speed_ratio < 0 or speed_ratio > 100:
            raise ValueError("Speed ratio must be within 0-100")
        self.feedback_level = feedback_level
        self.string_values = []
        self.float_values = [speed_ratio]


class GetControllerState(BaseInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetControllerState, self).__init__(
            {Interfaces.SYS: "get_controller_state"}, default_interface=Interfaces.SYS
        )
        self.feedback_level = feedback_level

    def on_after_receive(self, result, **kwargs):
        return result["string_values"][0]


class GetOperationMode(BaseInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetOperationMode, self).__init__({Interfaces.SYS: "get_operation_mode"}, default_interface=Interfaces.SYS)
        self.feedback_level = feedback_level

    def on_after_receive(self, result, **kwargs):
        return result["string_values"][0]


class GetExecutionState(BaseInstruction):
    def __init__(self, feedback_level=FeedbackLevel.DATA):
        super(GetExecutionState, self).__init__(
            {Interfaces.SYS: "get_execution_state"}, default_interface=Interfaces.SYS
        )
        self.feedback_level = feedback_level

    def on_after_receive(self, result, **kwargs):
        return result["string_values"][0]


# class GetTasks(BaseSystemInstruction):
#     def __init__(self, feedback_level=FeedbackLevel.DATA):
#         super(GetTasks, self).__init__(feedback_level)
#         self.instruction = 'get_tasks'

#     def parse_feedback(self, response):
#         return json.loads(response['feedback'])


# class GetTaskExecutionState(BaseSystemInstruction):
#     def __init__(self, task_name, feedback_level=FeedbackLevel.DATA):
#         super(GetTaskExecutionState, self).__init__(feedback_level)
#         self.instruction = 'get_task_execution_state'
#         self.string_values = [task_name]

#     def parse_feedback(self, response):
#         return response['string_values'][0]
