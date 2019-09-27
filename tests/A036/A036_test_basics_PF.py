from compas_rrc import *
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
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['t_A036_WG1_Robacta22'], feedback_level=1))
    print("Set Tool:", result['instruction'])

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['ob_A036_Workplace'], feedback_level=1))
    print("Set Workobject:", result['instruction'])

    # Set weldspeed start
    weldspeed = 11

    # Set weldjob start
    weldjob = 12

    # move to arc start position and start arc
    #result = abb.send_and_wait(ProjectInstruction('r_A036_ArcLStart', ['Test'], [80, 90, 100, 3.09086E-8, -0.707107, -0.707107, -3.09086E-8, -1700, 0, 0, 0, 0, 0, speed, Zone.FINE, weldspeed, weldjob], feedback_level=1))
    abb.send(ProjectInstruction('r_A036_ArcLStart',[], [80, 90, 100, 3.09086E-8, -0.707107, -0.707107, -3.09086E-8, -1700, 0, 0, 0, 0, 0, speed, Zone.FINE, weldspeed, weldjob]))

    # Set weldspeed pass position
    weldspeed = 12

    # Set weldjob pass position
    weldjob = 13

    # move to arc pass position
    abb.send(ProjectInstruction('r_A036_ArcL', [], [180, 90, 100, 3.09086E-8, -0.707107, -0.707107, -3.09086E-8, -1700, 0, 0, 0, 0, 0, speed, Zone.FINE, weldspeed, weldjob]))

    # Set weldspeed end
    weldspeed = 13

    # Set weldjob end
    weldjob = 14

    # move to arc end position and end arc
    abb.send(ProjectInstruction('r_A036_ArcLEnd', [], [80, 90, 100, 3.09086E-8, -0.707107, -0.707107, -3.09086E-8, -1700, 0, 0, 0, 0, 0, speed, Zone.FINE, weldspeed, weldjob]))

    # [80,90,0],[3.09086E-8,-0.707107,-0.707107,-3.09086E-8]
    # [-1700];
    # x 80, 90, 0, 3.09086E-8, -0.707107, -0.707107, -3.09086E-8, -1700, 0, 0, 0, 0, 0, speed, weldspeed, weldjob
    # y
    # z
    # q1
    # q2
    # q3
    # q4
    # e1
    # e2
    # e3
    # e4
    # e5
    # e6
    # speed
    # Zone
    # weldspeed
    # weldjob

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
