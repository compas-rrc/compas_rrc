from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time


def scan():
    result = abb.send_and_wait(ProjectInstruction('r_A014_Scan', feedback_level=1))
    distance = round(result['float_values'][0], 1)
    print('Distance = ', distance)

if __name__ == '__main__':

    stop = False

    ros = RosClient()

    abb = AbbClient(ros)
    abb.run()
    print('Connected.')
    print('')

    # set tool
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['t_A014_T1_rLaserSensor'], feedback_level=1))
    print('Tool set')

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['ob_A014_TestBase_Real'], feedback_level=1))
    print('Workobject set')

    # define orientation
    orientation = [0, 1, 0, 0]

    # move to 50mm
    result = abb.send_and_wait(MoveL(Frame.from_quaternion(orientation, [0, 0, -150]), [28000, -8500, -2600], 100, Zone.FINE, feedback_level=1))
    print('50 mm')

    # scann
    scan()

    # stop to teach 0V
    if stop == True :
        abb.send(ProjectInstruction('r_A042_Stop'))

    # move to 350mm
    result = abb.send_and_wait(MoveL(Frame.from_quaternion(orientation, [0, 0, 150]), [28000, -8500, -2600], 100, Zone.FINE, feedback_level=1))
    print('350 mm')

    # scann
    scan()

    # stop to teach 10V
    if stop == True :
        result = abb.send_and_wait(ProjectInstruction('r_A042_Stop', feedback_level=1))

    # move to 200mm
    result = abb.send_and_wait(MoveL(Frame.from_quaternion(orientation, [0, 0, 0]), [28000, -8500, -2600], 100, Zone.FINE, feedback_level=1))
    print('200 mm')

    # scann
    scan()

    # end of code
    print('')
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
