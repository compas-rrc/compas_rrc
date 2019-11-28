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
    if on:
        result = abb.send_and_wait(GetJointT(feedback_level=1))
        print(result)
        print(result.robot_joints)
        print(result.external_axes)

    # Get robtarget
    if off:
        result = abb.send_and_wait(GetRobT(feedback_level=1))
        print(result)

    # Move absolut joint
    if on:
        import math
        result = abb.send_and_wait(GetJointT(feedback_level=1))
        rob_axes = result.robot_joints
        ext_axes = result.external_axes
        rob_axes.values[0] += math.radians(5)
        print(rob_axes)
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
    if off:
        result = abb.send_and_wait(ReadAi('aiA032_CP1TubePr', feedback_level=1))
        print(result)

    # Read digital input
    if off:
        result = abb.send_and_wait(ReadDi('diA032_CP1Ready', feedback_level=1))
        print(result)

    # Read group input
    if off:
        result = abb.send_and_wait(ReadGi('giA014_T1AIn1Sta', feedback_level=1))
        print(result)

    # Reset digital output
    if off:
        result = abb.send_and_wait(ResetDo('doA032_AP1On', feedback_level=1))

    # SetAcc
    if off:
        result = abb.send_and_wait(SetAcc(33, 44, feedback_level=1))

    # Set analog output
    if off:
        result = abb.send_and_wait(SetAo('aoA032_AP1Speed', 225.75 , feedback_level=1))

    # Set digital output
    if off:
        result = abb.send_and_wait(SetDo('doA032_AP1On', feedback_level=1))

    # Set group output
    if off:
        result = abb.send_and_wait(SetGo('goA032_TestRRC', 255 , feedback_level=1))

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
    if off:
        result = abb.send_and_wait(WatchRead(feedback_level=1))
        print(result)

    # Watch start
    if off:
        result = abb.send_and_wait(WatchStart(feedback_level=1))
        #abb.send(WatchStart(feedback_level=0))


    # watch stop
    if off:
        result = abb.send_and_wait(WatchStop(feedback_level=1))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    # time.sleep(3)
