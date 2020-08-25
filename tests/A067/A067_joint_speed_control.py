import compas_rrc as rrc
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import time

if __name__ == '__main__':

    ros = RosClient("192.168.0.117")
    ros.run()

    robot_11 = rrc.AbbClient(ros, '/robot_1')
    robot_12 = rrc.AbbClient(ros, '/robot_2')

    print('Connected.')
    time.sleep(0.5)

    # Get joints
    robot_joints, external_axes = robot_12.send_and_wait(rrc.GetJoints())

    # Print received values
    print(robot_joints, external_axes)

    # Print confirm message to TP
    robot_12.send(rrc.PrintText('Press PLAY to execute'))
    robot_12.send(rrc.Stop())

    # Send a list of points
    points = [
        [[-6.91, -64.44, 27.17, -7.88, 7.84, -11.02], [23055.46, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.35, -61.24, 25.53, -6.28, 6.26, -12.35], [23055.46, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.53, -58.65, 24.09, -5.96, 5.09,  40.00], [23055.46, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.66, -55.73, 22.36, -6.19,  3.9, -12.28], [23055.46, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.75, -52.56, 20.34, -7.18, 2.75, -11.24], [23055.46, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        ]

    for robot_joints, external_axes in points:
        print ("sent:", robot_joints, external_axes)
        robot_12.send(rrc.MoveToJoints(robot_joints, external_axes, 30, rrc.Zone.Z1))

    robot_12.send(rrc.PrintText('Completed'))

    # end of code
    print('Finished')

    time.sleep(3)
    ros.terminate()
    time.sleep(3)
    print('ros terminated')
