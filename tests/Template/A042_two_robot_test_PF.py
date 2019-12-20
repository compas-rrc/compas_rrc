from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    ros = RosClient()
    ros.run()

    abb_r1 = AbbClient(ros, '/robot_1')
    abb_r2 = AbbClient(ros, '/robot_2')

    print('Connected.')

    # move robot one
    abb_r1.send_and_wait(MoveAbsJ([90, -55, 45, 180, -10, 45], [8000, -3200, -2500], 2000, Zone.FINE, feedback_level=1))
    abb_r1.send_and_wait(MoveAbsJ([90, -55, 45, 180, -10, 45], [8000, -4200, -2500], 2000, Zone.FINE, feedback_level=1))
    print('Finished 1')

    abb_r2.send_and_wait(MoveAbsJ([90, -55, 45, 180, -10, 45], [8000, -6200, -2500], 2000, Zone.FINE, feedback_level=1))
    abb_r2.send_and_wait(MoveAbsJ([90, -55, 45, 180, -10, 45], [8000, -7200, -2500], 2000, Zone.FINE, feedback_level=1))
    print('Finished 2')

    # end of code
    print('Finished')

    abb_r1.close()
    abb_r2.close()

    ros.terminate()

    time.sleep(3)
