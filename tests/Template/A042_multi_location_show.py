from compas_rrc import *
from compas_fab.backends.ros import RosClient

# ==============================================================================
# Temporary hot fix to speed up the feedback channel
from twisted.internet import reactor
reactor.timeout = lambda : 0.0001
# ==============================================================================

if __name__ == '__main__':

    # Switches for Code
    on = True
    off = False

    # Create Ros Client
    ros1 = RosClient()
    ros2 = RosClient(host='serveo.net')
    #ros3 = RosClient(host='rrc3.serveo.net')

    # Create ABB Client
    # abb_C51_R51 = AbbClient(ros1, '/C51_R51')
    # abb_vC51_R51 = AbbClient(ros1, '/vC51_R51')
    # abb_vC11_R11_R12 = AbbClient(ros, '/vC11_R11_R12')
    abb_vC11_R11 = AbbClient(ros2, '/vC11_R11')
    abb_vC11_R12 = AbbClient(ros2, '/vC11_R12')

    # run the eventloop on python to connect with ros
    ros2.run()
    print('Connected.')



    # Simple function check
    if on:

        # Print message on FlexPendant
        #done_C51_R51 = abb_C51_R51.send_and_wait(PrintText('C51_R51 '))
        #done_vC51_R51 = abb_vC51_R51.send_and_wait(PrintText('vC51_R51 '))
        done_vC11_R11 = abb_vC11_R11.send_and_wait(PrintText('vC11_R11 '))
        done_vC11_R12 = abb_vC11_R12.send_and_wait(PrintText('vC11_R12 '))

    # Show case step 1
    if off:

        # read position from real robot and gantry values from virtual robot
        robot_joints_C51_R51, external_axes_C51_R51 = abb_C51_R51.send_and_wait(GetJoints())
        print('Joints C51_R51', robot_joints_C51_R51, external_axes_C51_R51)

        robot_joints_vC11_R11, external_axes_vC11_R11 = abb_vC11_R11.send_and_wait(GetJoints())
        print('Joints vC11_R11', robot_joints_vC11_R11, external_axes_vC11_R11)

        robot_joints_vC11_R12, external_axes_vC11_R12 = abb_vC11_R12.send_and_wait(GetJoints())
        print('Joints vC11_R12', robot_joints_vC11_R12, external_axes_vC11_R12)

        # move virtual robots to real robot position exept gantry axis
        done_vC51_R51 = abb_vC51_R51.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_C51_R51, 100, Zone.FINE))
        print('done_vC51_R51')

        done_vC11_R11 = abb_vC11_R11.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_vC11_R11, 100, Zone.FINE))
        print('done_vC11_R11')

        done_vC11_R12 = abb_vC11_R12.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_vC11_R12, 100, Zone.FINE))
        print('done_vC11_R12')

    # Show case step 2
    if off:

        # Set multi move tasklist
        string_values, float_values = ['T_ROB11', 'T_ROB12'], []
        done_vC11_R11 = abb_vC11_R11.send_and_wait(CustomInstruction('r_A042_ABB_SetMultiMoveTasks', string_values, float_values))

        # Activate multi move
        string_values, float_values = [], []
        future_done_vC11_R11 = abb_vC11_R11.send(CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))
        future_done_vC11_R12 = abb_vC11_R12.send(CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))

        # Wait for feedback
        done_vC11_R11 = future_done_vC11_R11.result(timeout=5.0)
        done_vC11_R12 = future_done_vC11_R12.result(timeout=5.0)
        print('MultiMove On')

        # activate soft move on real robot
        abb_C51_R51.send(CustomInstruction('r_X000_ActSoftRobot'))

        # function to read the current position
        def get_joint_real_robot(result):

            robot_joints = result['float_values'][0:6]

            # send to vC51_R51
            abb_vC51_R51.send(MoveToJoints(robot_joints, external_axes_C51_R51, 2000, Zone.Z100))

            # send to vC11_R11 with multi move
            string_values = []
            float_values = list(robot_joints) + list(external_axes_vC11_R11) + [0, 0, 0] + [2000] + [Zone.Z100]
            abb_vC11_R11.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values, float_values, feedback_level=0))

            # send to vC11_R12 with multi move
            string_values = []
            float_values = list(robot_joints) + list(external_axes_vC11_R12) + [0, 0, 0] + [2000] + [Zone.Z100]
            abb_vC11_R12.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values, float_values, feedback_level=0))

        # subscribe real robot position
        abb_C51_R51.send_and_subscribe(Debug(CustomInstruction('r_A042_CyJobStart',['r_A042_GetJointT'],[0.25],exec_level=ExecutionLevel.MASTER)), get_joint_real_robot)

        # wait for user abort
        input('Press any key to finish!')

        done = abb_C51_R51.send_and_wait(CustomInstruction('r_A042_CyJobEnd',[],[],exec_level=ExecutionLevel.MASTER))
        print('Cyclic job ended', done)

        # deactivate soft move on real robot
        done = abb_C51_R51.send_and_wait(CustomInstruction('r_X000_DeactSoftRobot'))

        # Deactivate multi move
        string_values, float_values = [], []
        done_vC11_R11 = abb_vC11_R11.send(CustomInstruction('r_A042_ABB_MultiMoveOff', string_values, float_values, feedback_level=1))
        done_vC11_R12 = abb_vC11_R12.send(CustomInstruction('r_A042_ABB_MultiMoveOff', string_values, float_values, feedback_level=1))

        # Wait for feedback
        done_vC11_R11 = done_vC11_R11.result(timeout=5.0)
        done_vC11_R12 = done_vC11_R12.result(timeout=5.0)
        print('MultiMove Off')

    # End of Code
    print('Finished')

    # Close client
    #abb_C51_R51.close()
    #abb_vC51_R51.close()
    abb_vC11_R11.close()
    abb_vC11_R12.close()
    ros2.terminate()
