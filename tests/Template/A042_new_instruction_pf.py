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

    on = True
    off = False

    # Stop
    if off:
        abb.send(Stop())
        result = abb.send_and_wait(Stop(feedback_level=1))

    # WaitTime
    if off:
        abb.send(WaitTime(3))
        result = abb.send_and_wait(WaitTime(1.22, feedback_level=1))

    # SetDo and ResetDo
    if off:
        result = abb.send_and_wait(SetDo('doA032_AP1On', feedback_level=1))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(ResetDo('doA032_AP1On', feedback_level=1))

    # PulseDo
    if off:
        result = abb.send_and_wait(PulseDo('doA032_AP1On', 2.5, feedback_level=1))

    # SetTool
    if off:
        result = abb.send_and_wait(SetTool('t_A032_PrintNozzle', feedback_level=1))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(SetTool('tool0', feedback_level=1))

    # SetWobj (Workobject)
    if off:
        result = abb.send_and_wait(SetWobj('ob_A032_Pal2', feedback_level=1))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(SetWobj('wobj0', feedback_level=1))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
