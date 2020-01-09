from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # Switches for Code
    on = True
    off = False

    # No-op
    if off:
        result = abb.send_and_wait(Noop())
        print(result)

    # Get Joints
    if off:
        result = abb.send_and_wait(GetJoints())
        robot_joints, external_axes = result
        print(result)
        print(robot_joints)
        print(round(robot_joints.rax_1, 2))
        print(external_axes)
        print(external_axes.eax_a)


    # Get Frame
    if off:
        result = abb.send_and_wait(GetFrame())
        print(result)
        print(result.point)
        print(result.point.x)
        print(result.xaxis)
        print(result.xaxis.x)


    # Get Robtarget
    if off:
        frame, external_axes = abb.send_and_wait(GetRobtarget())
        print(frame)
        print(external_axes)


    # Move to Joints
    if off:
        robot_joints, external_axes = abb.send_and_wait(GetJoints())
        print(robot_joints.rax_3)
        robot_joints.rax_3 += 5
        print(robot_joints.rax_3)
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 500, Zone.FINE))
        print(done)

    # Move to Robtarget (Joint, Linear)
    if on:
        frame, ext_axes = abb.send_and_wait(GetRobtarget())
        print(frame.point.z)
        frame.point.z += 50
        print(frame.point.z)
        done = abb.send_and_wait(MoveToRobtarget(frame, ext_axes, 200, Zone.FINE))
        # done = abb.send_and_wait(MoveToRobtarget(frame, ext_axes, 200, Zone.FINE, Motion.JOINT))
        # done = abb.send_and_wait(MoveToRobtarget(frame, ext_axes, 200, Zone.FINE, Motion.LINEAR))


    # Pulse Digital
    if off:
        result = abb.send_and_wait(PulseDitital('doA032_AP1On', 2.5, feedback_level=1))

    # Read Analog
    if off:
        result = abb.send_and_wait(ReadAnalog('aiA032_CP1TubePr'))
        print(result)

    # Read Digital
    if off:
        result = abb.send_and_wait(ReadDigital('diA032_CP1Ready'))
        print(result)

    # Read Group
    if off:
        result = abb.send_and_wait(ReadGroup('giA014_T1AIn1Sta'))
        print(result)

    # Set Accleration
    if off:
        result = abb.send_and_wait(SetAccleration(33, 44))

    # Set Analog
    if off:
        result = abb.send_and_wait(SetAnalog('aoA032_AP1Speed', 225.75))

    # Set Digital
    if off:
        result = abb.send_and_wait(SetDigital('doA032_AP1On', 1))

    # Set Group
    if off:
        result = abb.send_and_wait(SetGroup('goA032_TestRRC', 255))

    # Set Tool
    if off:
        result = abb.send_and_wait(SetTool('t_A032_PrintNozzle'))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(SetTool('tool0'))

    # Set Max Speed
    if off:
        result = abb.send_and_wait(SetMaxSpeed(2500))

    # Set Work Object
    if off:
        result = abb.send_and_wait(SetWobj('ob_A032_Pal2'))
        abb.send(WaitTime(3))
        result = abb.send_and_wait(SetWobj('wobj0'))

    # Stop Task
    if off:
        result = abb.send_and_wait(Stop())

    # Print Text
    if off:
        result = abb.send_and_wait(PrintText('Compas RCC'))

    # Wait Time
    if off:
        result = abb.send_and_wait(WaitTime(3))

    # Read Watch
    if off:
        result = abb.send_and_wait(ReadWatch())
        print(result)

    # Start Watch
    if off:
        result = abb.send_and_wait(StartWatch())

    # Stop watch
    if off:
        result = abb.send_and_wait(StopWatch())

    # CustomInstruction
    if off:
        pass
        #result = abb.send_and_wait(WatchStop(feedback_level=1))

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
