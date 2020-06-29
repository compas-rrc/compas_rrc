from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb_vc11_r11 = AbbClient(ros, '/vC11_R11')
    abb_vc11_r12 = AbbClient(ros, '/vC11_R12')
    abb_vc21_r21 = AbbClient(ros, '/vC21_R21')
    abb_vc21_r22 = AbbClient(ros, '/vC21_R22')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Switches for Code
    on = True
    off = False

    # Move robot 11
    if on:

        # Set robot
        abb = abb_vc11_r11

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change any value and move to new position
        robot_joints.rax_1 += 15
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        # Message done
        print('done : ', abb)

    # Move robot 12
    if on:

        # Set robot
        abb = abb_vc11_r12

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change any value and move to new position
        robot_joints.rax_1 += 15
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        # Message done
        print('done : ', abb)

    # Move robot 21
    if on:

        # Set robot
        abb = abb_vc21_r21

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change any value and move to new position
        robot_joints.rax_1 += 15
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        # Message done
        print('done : ', abb)

    # Move robot 22
    if on:

        # Set robot
        abb = abb_vc21_r22

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change any value and move to new position
        robot_joints.rax_1 += 15
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        # Message done
        print('done : ', abb)

    # End of Code
    print('Finished')

    # Close client
    # abb_vc11_r11.close()
    # abb_vc11_r12.close()
    # abb_vc21_r21.close()
    # abb_vc21_r22.close()
    ros.terminate()
