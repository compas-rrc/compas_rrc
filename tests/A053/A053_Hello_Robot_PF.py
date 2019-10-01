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

    # set tool
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['tool0'], feedback_level=1))
    print("Set Tool:", result['instruction'])

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['wobj0'], feedback_level=1))
    print("Set Workobject:", result['instruction'])

    # get robtarget
    feedback_getpos = abb.send_and_wait(ProjectInstruction('r_A042_GetRobT',feedback_level=1))
    print("Feedback get pos:",feedback_getpos)

    current_pos = feedback_getpos['float_values'][17:-1]
    x = current_pos[0]
    y = current_pos[1]
    z = current_pos[2]

    q1 = current_pos[3]
    q2 = current_pos[4]
    q3 = current_pos[5]
    q4 = current_pos[6]

    y = -200

    result = abb.send_and_wait(ProjectInstruction('r_A042_MoveJ', [], [x, y, z, q1, q2, q3, q4, 0, 0, 0, 0, 0, 0, 500, Zone.FINE], feedback_level=1))

    print("Current position:",current_pos)

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
