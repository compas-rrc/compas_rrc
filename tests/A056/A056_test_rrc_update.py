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

    # Switches for Code
    on = True
    off = False

    # Get and move robot 1
    if on:

        abb = abb_r1

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change any value and move to new position
        robot_joints.rax_1 += 15
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        for i in range(15):
            print(i+1)
            robot_joints.rax_1 -= 1
            print(robot_joints.rax_1)
            # done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))
            abb.send(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())
        print(robot_joints, external_axes)

    # end of code
    print('Finished')

    ros.terminate()

    time.sleep(3)
