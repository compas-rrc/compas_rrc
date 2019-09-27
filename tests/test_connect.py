from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import time

if __name__ == '__main__':
    abb = AbbClient(RosClient())
    abb.run()
    print('Connected.')
    time.sleep(2)
    inst = MoveAbsJ([90, 45, 0, 1, 10, 20], [22000, -6500, -4500], 2000, Zone.FINE, feedback_level=1)
    feedback = abb.send(inst)
    result = feedback.result(3)
    print(result)
    # result = abb.send_and_wait(inst, 3)
    # print(result)
    # abb.send_and_wait(MoveAbsJ([90, 45, 0, 1, 10, 20], [22000, -6500, -4500], 2000, Zone.FINE, feedback_level=1))

    print('Closing connection')

    abb.close()

    print('Terminating loop')
    time.sleep(1)
    abb.terminate()
