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
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['t_A014_T1LaserSensor'], feedback_level=1))
    print("Set Tool:", result['instruction'])

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['ob_A014_TestBase'], feedback_level=1))
    print("Set Workobject:", result['instruction'])

    # move to scan position
    abb.send(MoveAbsJ([90, -55, 45, 180, -10, 45], [28000, -5200, -2500], speed, Zone.FINE))

    # scan
    future = abb.send(ProjectInstruction('r_A014_Scan', feedback_level=1))

    # move from scan position away
    abb.send(MoveAbsJ([90, -55, 45, 180, -10, 45], [28000, -5300, -2500], speed, Zone.FINE))

    # catch feedback future from scan and print important parameters
    result = future.result()
    print("Distance:", result['float_values'][0])
    print("Measure feedback:", result['string_values'][0])

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
