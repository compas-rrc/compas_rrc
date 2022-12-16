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


# class BaseSystemInstruction(ROSmsg, SystemInstruction):
#     def __init__(self, feedback_level=FeedbackLevel.DATA, execution_level=ExecutionLevel.DRIVER):
#         super(BaseSystemInstruction, self).__init__()
#         self.feedback_level = feedback_level
#         self.exec_level = execution_level
#         self.string_values = []
#         self.float_values = []


# class SystemCustomInstruction(BaseSystemInstruction):
#     def __init__(self, name, method="GET", data=None, feedback_level=FeedbackLevel.DATA):
#         super(SystemCustomInstruction, self).__init__(feedback_level)
#         if data is not None:
#             method = "POST"
#         self.instruction = json.dumps(dict(path=name, method=method, data=data))

#     def parse_feedback(self, response):
#         return json.loads(response["feedback"])


# class SystemGetVariable(BaseSystemInstruction):
#     def __init__(self, variable_name, task_name, feedback_level=FeedbackLevel.DATA):
#         super(SystemGetVariable, self).__init__(feedback_level)
#         self.instruction = 'get_rapid_variable'
#         self.string_values = [variable_name, task_name]

#     def parse_feedback(self, response):
#         if len(response['string_values']):
#             return response['string_values'][0]
#         elif len(response['float_values']):
#             return response['float_values'][0]
#         else:
#             raise Exception('Invalid response, no value returned')


# class SystemSetVariable(BaseSystemInstruction):
#     def __init__(self, variable_name, variable_value, task_name, feedback_level=FeedbackLevel.DATA):
#         super(SystemSetVariable, self).__init__(feedback_level)
#         self.instruction = 'set_rapid_variable'
#         variable_value = json.dumps(variable_value)
#         self.string_values = [variable_name, variable_value, task_name]


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
