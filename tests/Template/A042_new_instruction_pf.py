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

    # Dummy
    if off:
        result = abb.send_and_wait(Dummy(feedback_level=1))

    # GetJointT
    if off:
        result = abb.send_and_wait(GetJointT(feedback_level=1))
        print()
        print('Roboter Joint 1 =', round(result['float_values'][18],2))
        print('Roboter Joint 2 =', round(result['float_values'][19],2))
        print('Roboter Joint 3 =', round(result['float_values'][20],2))
        print('Roboter Joint 4 =', round(result['float_values'][21],2))
        print('Roboter Joint 5 =', round(result['float_values'][22],2))
        print('Roboter Joint 6 =', round(result['float_values'][23],2))
        print()
        print('Gantry Joint X =', round(result['float_values'][24],2))
        print('Gantry Joint Y =', round(result['float_values'][25],2))
        print('Gantry Joint Z =', round(result['float_values'][26],2))
        print()

    # GetRobT
    if on:
        result = abb.send_and_wait(GetRobT(feedback_level=1))
        print()
        print('Pos X =', round(result['float_values'][17],2))
        print('Pos y =', round(result['float_values'][18],2))
        print('Pos z =', round(result['float_values'][19],2))
        print('Orient q1 =', round(result['float_values'][20],2))
        print('Orient q2 =', round(result['float_values'][21],2))
        print('Orient q3 =', round(result['float_values'][22],2))
        print('Orient q4 =', round(result['float_values'][23],2))
        print()
        print('Gantry Joint X =', round(result['float_values'][24],2))
        print('Gantry Joint Y =', round(result['float_values'][25],2))
        print('Gantry Joint Z =', round(result['float_values'][26],2))
        print()

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

    # SetAcc
    if off:
        result = abb.send_and_wait(SetAcc(33, 44, feedback_level=1))

    # SetVel
    if off:
        result = abb.send_and_wait(SetVel(99, 2500, feedback_level=1))

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

    # TPWrite
    if off:
        result = abb.send_and_wait(TPWrite('Compas RCC', feedback_level=1))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
