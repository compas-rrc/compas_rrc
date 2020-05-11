from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb_C51_R51 = AbbClient(ros, '/C51_R51')
    abb_vC51_R51 = AbbClient(ros, '/vC51_R51')
    # abb_vC11_R11_R12 = AbbClient(ros, '/vC11_R11_R12')
    abb_vC11_R11 = AbbClient(ros, '/vC11_R11')
    abb_vC11_R12 = AbbClient(ros, '/vC11_R12')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Switches for Code
    on = True
    off = False

    # Simple function check
    if on:

        # Print message on FlexPendant
        done_C51_R51 = abb_C51_R51.send_and_wait(PrintText('C51_R51 '))
        done_vC51_R51 = abb_vC51_R51.send_and_wait(PrintText('vC51_R51 '))
        done_vC11_R11 = abb_vC11_R11.send_and_wait(PrintText('vC11_R11 '))
        done_vC11_R12 = abb_vC11_R12.send_and_wait(PrintText('vC11_R12 '))

    # Read position from real robot and and move vitrual robot in the same position
    if off:

        # read position from real robot
        robot_joints, external_axes = abb_C51_R51.send_and_wait(GetJoints())

        # move virtual robot
        virtual_robot_in_real_robot_positon = abb_vC51_R51.send_and_wait(MoveToJoints(robot_joints, external_axes, 100, Zone.FINE))

    # Show case
    if off:

        # activate soft move on real robot
        abb_C51_R51.send(CustomInstruction('r_X000_ActSoftRobot'))

        # function to read the current position
        def get_joint_real_robot(result):

            robot_joints = result['float_values'][0:6]
            external_axes = []
            abb_vC51_R51.send(MoveToJoints(robot_joints, external_axes, 200, Zone.Z10))


        # subscribe real robot position
        abb_C51_R51.send_and_subscribe(Debug(CustomInstruction('r_A042_CyJobStart',['r_A042_GetJointT'],[0.5],exec_level=ExecutionLevel.MASTER)), get_joint_real_robot)

        # wait for user abort
        input('Press any key to finish!')

        done = abb_C51_R51.send_and_wait(CustomInstruction('r_A042_CyJobEnd',[],[],exec_level=ExecutionLevel.MASTER))
        print('Cyclic job ended', done)

        # deactivate soft move on real robot
        abb_C51_R51.send(CustomInstruction('r_X000_DeactSoftRobot'))

    # End of Code
    print('Finished')

    # Close client
    abb_C51_R51.close()
    abb_vC51_R51.close()
    abb_vC11_R11.close()
    abb_vC11_R12.close()
    ros.terminate()
