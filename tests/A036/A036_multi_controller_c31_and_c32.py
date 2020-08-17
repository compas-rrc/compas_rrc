from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb_vc31_r31 = AbbClient(ros, '/vC31_R31')
    abb_vc32_r32 = AbbClient(ros, '/vC32_R32')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Switches for Code
    on = True
    off = False

    # Move robot 31
    if on:

        # Set robot
        abb = abb_vc31_r31

        # Get joints
        robot_joints, external_axes = abb.send_and_wait(GetJoints())

        # Print received values
        print(robot_joints, external_axes)

        # Change any value and move to new position
        robot_joints.rax_1 += 15
        done = abb.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

        # Message done
        print('done : ', abb)

    # Move robot 32
    if on:

        # Set robot
        abb = abb_vc32_r32

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
    # abb_vc31_r31.close()
    # abb_vc32_r32.close()
    ros.terminate()
