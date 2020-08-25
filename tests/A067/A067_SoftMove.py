import compas_rrc as rrc
from compas.geometry import Frame, Vector
from compas_fab.backends.ros import RosClient
import time

if __name__ == '__main__':

    ros = RosClient("192.168.0.117")
    ros.run()

    robot_11 = rrc.AbbClient(ros, '/robot_1')
    robot_12 = rrc.AbbClient(ros, '/robot_2')

    print('Connected.')
    time.sleep(0.5)



    # Set Tool
    # robot_12.send(rrc.SetWorkObject('wobj0'))
    robot_12.send(rrc.SetTool('t_A067_T1_Gripper'))

    # Print confirm message to TP
    robot_12.send(rrc.PrintText('Press PLAY to start SoftMove'))
    robot_12.send(rrc.Stop())

    # Read current Robot Frame
    frame_start, ext_axes = robot_12.send_and_wait(rrc.GetRobtarget())

    # Settings for Soft Move
    soft_direction = "Z"            # soft_direction modes available are "Z", "XY", "XYZ"
    stiffness = 99                   # Stiffness in the specified direction, 0 is softest, 100 is stiffness
    stiffness_non_soft_dir = 100     # Stiffness in the other non specified direction, 0 is softest, 100 is stiffness
    print ("sending : r_A067_ActSoftMove", soft_direction, stiffness, stiffness_non_soft_dir)
    robot_12.send(rrc.CustomInstruction("r_A067_ActSoftMove", string_values=[soft_direction], float_values=[stiffness, stiffness_non_soft_dir]))

    # Translate frame along Z direction and send it back to Robot
    distance = 200
    frame_target = Frame(frame_start.point + frame_start.zaxis * distance, frame_start.xaxis, frame_start.yaxis)
    robot_12.send(rrc.MoveToRobtarget(frame_target, ext_axes, 20, rrc.Zone.FINE))
    print("Target", frame_target, ext_axes)

    # input ("Press something to continue...")

    # robot_12.send(rrc.PrintText('Press PLAY to stop SoftMove'))
    # robot_12.send(rrc.Stop())
    robot_12.send(rrc.CustomInstruction("r_A067_DeactSoftMove"))

    # Read current Robot Frame
    frame_end, ext_axes = robot_12.send_and_wait(rrc.GetRobtarget())
    print("End Position", frame_end, ext_axes)
    # Print out error from target
    print("Error from target :", Vector.from_start_end(frame_end.point, frame_target.point).length)

    # Send the robot to its original position before terminating the test.
    robot_12.send(rrc.MoveToRobtarget(frame_start, ext_axes, 50, rrc.Zone.FINE))

    # end of code
    print('Finished')

    time.sleep(3)
    ros.terminate()
    time.sleep(3)
    print('ros terminated')
