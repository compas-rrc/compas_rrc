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

    # MoveAbsJ
    abb.send(MoveAbsJ([0, 45, 45, 0, 45, 0], [28000, -4000, -2600], 2500, Zone.FINE))
    fb_move_abs_j = abb.send_and_wait(MoveAbsJ([0, -45, 45, 0, 45, 0], [28000, -4000, -2600], 2500, Zone.FINE, feedback_level=1))
    print('Feedback MoveAbsJ = ', fb_move_abs_j)
    print(fb_move_abs_j('feedback'))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
