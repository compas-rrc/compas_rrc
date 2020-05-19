from compas_rrc import *
from compas_fab.backends.ros import RosClient

# ==============================================================================
# Temporary hot fix to speed up the feedback channel
from twisted.internet import reactor
reactor.timeout = lambda : 0.0001
# ==============================================================================

if __name__ == '__main__':

    # Switches for locations
    location_einsiedeln = True
    location_forch = True
    location_zurich = True

    # Switches for function
    connection_test = True
    show_step_1 = True
    show_step_2 = True


    if location_einsiedeln:

        # Create Ros Client
        ros_einsiedeln_philippe_fleischmann = RosClient()

        # Create ABB Client
        abb_C51_R51 = AbbClient(ros_einsiedeln_philippe_fleischmann, '/C51_R51')

        # run the eventloop on python to connect with ros
        ros_einsiedeln_philippe_fleischmann.run()

        # User informantion
        print('Einsiedeln - Philippe Fleischmann - Connected')


    if location_forch:

        # Create Ros Client
        ros_forch_gonzalo_casas = RosClient(host='rrc-forch.serveo.net', port=9091)

        # Create ABB Client
        abb_vC11_R11 = AbbClient(ros_forch_gonzalo_casas, '/vC11_R11')
        abb_vC11_R12 = AbbClient(ros_forch_gonzalo_casas, '/vC11_R12')

        # run the eventloop on python to connect with ros
        ros_forch_gonzalo_casas.run()

        # User informantion
        print('Forch - Gonzalo Casas - Connected')


    if location_zurich:

        # Create Ros Client
        ros_zurich_michael_lyrenmann = RosClient(host='rrc-zurich.serveo.net')

        # Create ABB Client
        abb_C11_R11 = AbbClient(ros_zurich_michael_lyrenmann, '/C11_R11')
        abb_C11_R12 = AbbClient(ros_zurich_michael_lyrenmann, '/C11_R12')

        # run the eventloop on python to connect with ros
        ros_zurich_michael_lyrenmann.run()

        # User informantion
        print('Zurich - Michael Lyrenmann - Connected')


    if connection_test and location_einsiedeln:

        # Print message on FlexPendant
        done_C51_R51 = abb_C51_R51.send_and_wait(PrintText('C51_R51 '))

    if connection_test and location_forch:

        # Print message on FlexPendant
        done_vC11_R11 = abb_vC11_R11.send_and_wait(PrintText('vC11_R11 '))
        done_vC11_R12 = abb_vC11_R12.send_and_wait(PrintText('vC11_R12 '))

    if connection_test and location_zurich:

        # Print message on FlexPendant
        done_C11_R11 = abb_C11_R11.send_and_wait(PrintText('C11_R11 '))
        done_C11_R12 = abb_C11_R12.send_and_wait(PrintText('C11_R12 '))

    # Show case step 1
    if show_step_1:

        # read position from real robot and gantry values from virtual robot
        robot_joints_C51_R51, external_axes_C51_R51 = abb_C51_R51.send_and_wait(GetJoints())
        print('Joints C51_R51', robot_joints_C51_R51, external_axes_C51_R51)

        robot_joints_vC11_R11, external_axes_vC11_R11 = abb_vC11_R11.send_and_wait(GetJoints())
        print('Joints vC11_R11', robot_joints_vC11_R11, external_axes_vC11_R11)

        robot_joints_vC11_R12, external_axes_vC11_R12 = abb_vC11_R12.send_and_wait(GetJoints())
        print('Joints vC11_R12', robot_joints_vC11_R12, external_axes_vC11_R12)

        robot_joints_C11_R11, external_axes_C11_R11 = abb_C11_R11.send_and_wait(GetJoints())
        print('Joints C11_R11', robot_joints_C11_R11, external_axes_C11_R11)

        robot_joints_C11_R12, external_axes_C11_R12 = abb_C11_R12.send_and_wait(GetJoints())
        print('Joints C11_R12', robot_joints_C11_R12, external_axes_C11_R12)

        # move robots to master position exept gantry axis

        done_vC11_R11 = abb_vC11_R11.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_vC11_R11, 100, Zone.FINE))
        print('done_vC11_R11')

        done_vC11_R12 = abb_vC11_R12.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_vC11_R12, 100, Zone.FINE))
        print('done_vC11_R12')

        done_C11_R11 = abb_C11_R11.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_C11_R11, 100, Zone.FINE))
        print('done_C11_R11')

        done_C11_R12 = abb_C11_R12.send_and_wait(MoveToJoints(robot_joints_C51_R51, external_axes_C11_R12, 100, Zone.FINE))
        print('done_C11_R12')

    # Show case step 2
    if show_step_2:

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

        # User informantion
        print('MultiMove vC11_R11_R12_On')


        # Set multi move tasklist
        string_values, float_values = ['T_ROB11', 'T_ROB12'], []
        done_C11_R11 = abb_C11_R11.send_and_wait(CustomInstruction('r_A042_ABB_SetMultiMoveTasks', string_values, float_values))

        # Activate multi move
        string_values, float_values = [], []
        future_done_C11_R11 = abb_C11_R11.send(CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))
        future_done_C11_R12 = abb_C11_R12.send(CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))

        # Wait for feedback
        done_C11_R11 = future_done_C11_R11.result(timeout=5.0)
        done_C11_R12 = future_done_C11_R12.result(timeout=5.0)

        # User informantion
        print('MultiMove C11_R11_R12_On')


        # activate soft move on real robot
        abb_C51_R51.send(CustomInstruction('r_X000_ActSoftRobot'))

        # function to read the current position
        def get_joint_real_robot(result):

            robot_joints = result['float_values'][0:6]

            # send to vC11_R11 with multi move
            string_values = []
            float_values = list(robot_joints) + list(external_axes_vC11_R11) + [0, 0, 0] + [2000] + [Zone.Z100]
            abb_vC11_R11.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values, float_values, feedback_level=0))

            # send to vC11_R12 with multi move
            string_values = []
            float_values = list(robot_joints) + list(external_axes_vC11_R12) + [0, 0, 0] + [2000] + [Zone.Z100]
            abb_vC11_R12.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values, float_values, feedback_level=0))

            # send to C11_R11 with multi move
            string_values = []
            float_values = list(robot_joints) + list(external_axes_C11_R11) + [0, 0, 0] + [2000] + [Zone.Z100]
            abb_C11_R11.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values, float_values, feedback_level=0))

            # send to C11_R12 with multi move
            string_values = []
            float_values = list(robot_joints) + list(external_axes_C11_R12) + [0, 0, 0] + [2000] + [Zone.Z100]
            abb_C11_R12.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values, float_values, feedback_level=0))

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
        done_vC11_R11 = done_vC11_R11.result(timeout=25.0)
        done_vC11_R12 = done_vC11_R12.result(timeout=25.0)
        print('MultiMove vC11_R11_R12 Off')

        # Deactivate multi move
        string_values, float_values = [], []
        done_C11_R11 = abb_C11_R11.send(CustomInstruction('r_A042_ABB_MultiMoveOff', string_values, float_values, feedback_level=1))
        done_C11_R12 = abb_C11_R12.send(CustomInstruction('r_A042_ABB_MultiMoveOff', string_values, float_values, feedback_level=1))

        # Wait for feedback
        done_C11_R11 = done_C11_R11.result(timeout=5.0)
        done_C11_R12 = done_C11_R12.result(timeout=5.0)
        print('MultiMove C11_R11_R12 Off')

    # End of Code
    print('Finished')


    if location_einsiedeln:

        # Close client
        abb_C51_R51.close()
        ros_einsiedeln_philippe_fleischmann.terminate()


    if location_forch:

        # Close client
        abb_vC11_R11.close()
        abb_vC11_R12.close()
        ros_forch_gonzalo_casas.terminate()


    if location_zurich:

        # Close client
        abb_C11_R11.close()
        abb_C11_R12.close()
        ros_zurich_michael_lyrenmann.terminate()
