from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb_c51 = AbbClient(ros, '/C51')
    abb_vc51 = AbbClient(ros, '/vC51')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Switches for Code
    on = True
    off = False

    # Simple function check
    if off:

        # Print message on FlexPendant
        done_c51 = abb_c51.send_and_wait(PrintText('C51 Robot 1 '))
        done_vc51 = abb_vc51.send_and_wait(PrintText('vC51 Robot 1 '))

    # Read position from real robot and and move vitrual robot in the same position
    if on:

        # read position from real robot
        robot_joints, external_axes = abb_c51.send_and_wait(GetJoints())

        # move virtual robot
        virtual_robot_in_real_robot_positon = abb_vc51.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

    # Show case
    if off:

        # Deactivate soft servo on robot
        # abb.send(CustomInstruction('r_X000_DeactSoftRobot'))
        def get_joint_received(result):
            print(result)

        abb.send_and_subscribe(Debug(CustomInstruction('r_A042_CyJobStart',['r_A042_GetJointT'],[0.01],exec_level=ExecutionLevel.MASTER)), get_joint_received)

        # wait for user abort
        input('Press any key to finish!')

        done = abb.send_and_wait(CustomInstruction('r_A042_CyJobEnd',[],[],exec_level=ExecutionLevel.MASTER))
        print('Cyclic job ended', done)


    # End of Code
    print('Finished')

    # Close client
    abb_c51.close()
    abb_vc51.close()
    ros.terminate()
