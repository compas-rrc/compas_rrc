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

    # set tool
    abb.send(ProjectInstruction('r_A042_SetTool', ['t_A036_WG1_Robacta22']))

    # set workobject
    abb.send(ProjectInstruction('r_A042_SetWorkobject', ['ob_A036_Workplace']))

    # stop befor moving
    abb.send(ProjectInstruction('r_A036_Stop'))

    # Set position
    x = 260
    y = 200
    z = 0
    q1 = 3.09086E-8
    q2 = -0.707107
    q3 = -0.707107
    q4 = -3.09086E-8
    eAx1 = -1700
    eAx2 = 0
    eAx3 = 0
    eAx4 = 0
    eAx5 = 0
    eAx6 = 0

    # Move parameters
    speed = 200 # mm/s
    zone = Zone.FINE

    # Set weldspeed start
    weldspeed = 1

    # Set weldjob start
    weldjob = 2

    # Set instruction
    instruction = 'r_A042_MoveL'

    # Set position
    z = 50

    # move to the pre position
    abb.send(ProjectInstruction(instruction,[], [x, y, z, q1, q2, q3, q4, eAx1, eAx2, eAx3, eAx4, eAx5, eAx6, speed, zone]))

    # Set instruction
    instruction = 'r_A036_ArcLStart'

    # Set position
    z = 0

    # move to arc start position and start the arc
    abb.send(ProjectInstruction(instruction,[], [x, y, z, q1, q2, q3, q4, eAx1, eAx2, eAx3, eAx4, eAx5, eAx6, speed, zone, weldspeed, weldjob]))

    # Set instruction
    instruction = 'r_A036_ArcLEnd'

    # Set position
    z = 2

    # move to arc end position and end the arc
    abb.send(ProjectInstruction(instruction,[], [x, y, z, q1, q2, q3, q4, eAx1, eAx2, eAx3, eAx4, eAx5, eAx6, speed, zone, weldspeed, weldjob]))

    # Set instruction
    instruction = 'r_A042_MoveL'

    # Set position
    z = 50

    # move to post position
    abb.send(ProjectInstruction(instruction,[], [x, y, z, q1, q2, q3, q4, eAx1, eAx2, eAx3, eAx4, eAx5, eAx6, speed, zone]))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
