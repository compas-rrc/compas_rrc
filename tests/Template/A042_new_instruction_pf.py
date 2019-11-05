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

    # Get jointtarget
    if off:
        result = abb.send_and_wait(GetJointT(feedback_level=1))
        print(result)

    # Get robtarget
    if off:
        result = abb.send_and_wait(GetRobT(feedback_level=1))
        print(result)

    # Move absolut joint
    if off:
        current_joints = abb.send_and_wait(GetJointT(feedback_level=1))
        rob_axes = current_joints[0]
        ext_axes = current_joints[1]
        rob_axes[0] = rob_axes[0] + 5
        print(current_joints)
        print(rob_axes)
        print(ext_axes)
        done = abb.send_and_wait(MoveAbsJ(rob_axes, ext_axes, 200, Zone.FINE,feedback_level=1))
        print(done)

    # Move joint
    if off:
        current_robtarget = abb.send_and_wait(GetRobT(feedback_level=1))
        current_joints = abb.send_and_wait(GetJointT(feedback_level=1))
        ext_axes = current_joints[1]
        current_robtarget.point[2] = current_robtarget.point[2] + 50
        print(current_robtarget.point)
        done = abb.send_and_wait(MoveJ(current_robtarget, ext_axes, 200, Zone.FINE,feedback_level=1))

    # Move linear
    if off:
        current_robtarget = abb.send_and_wait(GetRobT(feedback_level=1))
        current_joints = abb.send_and_wait(GetJointT(feedback_level=1))
        ext_axes = current_joints[1]
        current_robtarget.point[2] = current_robtarget.point[2] + 50
        print(current_robtarget.point)
        done = abb.send_and_wait(MoveL(current_robtarget, ext_axes, 200, Zone.FINE,feedback_level=1))

    # PulseDo
    if off:
        result = abb.send_and_wait(PulseDo('doA032_AP1On', 2.5, feedback_level=1))

    # Read analog input

    # Read digital input

    # Read group input

    # Reset digital output

    # SetAcc
    if off:
        result = abb.send_and_wait(SetAcc(33, 44, feedback_level=1))

    # Set analog output

    # Set digital output
    # SetDo and ResetDo
    if off:
        result = abb.send_and_wait(SetDo('doA032_AP1On', feedback_level=1))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(ResetDo('doA032_AP1On', feedback_level=1))

    # Set group output

    # Set tool
    if off:
        result = abb.send_and_wait(SetTool('t_A032_PrintNozzle', feedback_level=1))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(SetTool('tool0', feedback_level=1))

    # SetVel
    if off:
        result = abb.send_and_wait(SetVel(99, 2500, feedback_level=1))

    # Set workobject
    if off:
        result = abb.send_and_wait(SetWobj('ob_A032_Pal2', feedback_level=1))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(SetWobj('wobj0', feedback_level=1))

    # Stop
    if off:
        abb.send(Stop())
        result = abb.send_and_wait(Stop(feedback_level=1))

    # TPWrite
    if off:
        result = abb.send_and_wait(TPWrite('Compas RCC', feedback_level=1))

    # Wait time
    if off:
        abb.send(WaitTime(3))
        result = abb.send_and_wait(WaitTime(1.22, feedback_level=1))

    # Watch read

    # Watch start

    # watch stop


    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    # time.sleep(3)
