from abb_a042_base_lib import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    ros = RosClient()

    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # set speed
    speed = 500

    # set tool
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['t_A014_T1LaserSensor'],feedback_level=1))
    print("Set Tool:",result['instruction'])

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['ob_A014_TestBase'],feedback_level=1))
    print("Set Workobject:",result['instruction'])

    # get robtarget
    current_pos = abb.send_and_wait(ProjectInstruction('r_A042_GetRobT',feedback_level=1))
    print("Current position:",current_pos)

    Current position: {'float_values': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 496.5726013183594, 340.8928527832031, 343.11944580078125, 2.5251551960536744e-06, -0.7071056365966797, 0.7071079611778259, -1.1295470869754354e-07, 28000.01171875, -3700.000244140625, -2800.000244140625], 'feedback_level': 0, 'feedback': 'Done FError 1', 'instruction': 'r_A042_GetRobT', 'feedback_id': 3, 'sequence_id': 3, 'exec_level': 0, 'string_values': []}

    # move to scan position
    # abb.send(MoveAbsJ([90, -55, 45, 180, -10, 45], [28000, -5200, -2500], speed, Zone.FINE))


    # scan
    # future = abb.send(ProjectInstruction('r_A014_Scan',feedback_level=1))

    # move from scan position away
    # abb.send(MoveAbsJ([90, -55, 45, 180, -10, 45], [28000, -5300, -2500], speed, Zone.FINE))

    # catch feedback future from scan and print important parameters
    # result = future.result()
    # print("Distance:", result['float_values'][0])
    # print("Measure feedback:", result['string_values'][0])

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
