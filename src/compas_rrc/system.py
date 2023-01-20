# import json

# from compas_fab.backends.ros.messages import ROSmsg

# from compas_rrc.common import ExecutionLevel
# from compas_rrc.common import FeedbackLevel

__all__ = [
    # 'GetControllerState',
    # 'GetSpeedRatio',
    # 'GetTaskExecutionState',
    # 'GetTasks',
    # 'SystemCustomInstruction',
    # 'SystemGetVariable',
    # 'SystemSetVariable',
    # 'SystemStart',
    # 'SystemStop',
]


# class GetControllerState(BaseSystemInstruction):
#     def __init__(self, feedback_level=FeedbackLevel.DATA):
#         super(GetControllerState, self).__init__(feedback_level)
#         self.instruction = 'get_controller_state'

#     def parse_feedback(self, response):
#         return response['string_values'][0]


# class GetSpeedRatio(BaseSystemInstruction):
#     def __init__(self, feedback_level=FeedbackLevel.DATA):
#         super(GetSpeedRatio, self).__init__(feedback_level)
#         self.instruction = 'get_speed_ratio'

#     def parse_feedback(self, response):
#         return response['float_values'][0]


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
