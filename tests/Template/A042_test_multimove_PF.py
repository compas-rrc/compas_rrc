from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    ros = RosClient()
    ros.run()

    abb_r1 = AbbClient(ros, '/robot_1')
    abb_r2 = AbbClient(ros, '/robot_2')

    print('Connected.')

    # Set multi move tasklist
    string_values, float_values = ['T_ROB11', 'T_ROB12'], []
    done_r1 = abb_r1.send_and_wait(CustomInstruction('r_A042_ABB_SetMultiMoveTasks', string_values, float_values))

    # Activate multi move
    string_values, float_values = [], []
    future_done_r1 = abb_r1.send(CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))
    future_done_r2 = abb_r2.send(CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))

    # Wait for feedback
    done_r1 = future_done_r1.result(timeout=5.0)
    done_r1 = future_done_r2.result(timeout=5.0)
    print('MultiMove On')

    # Get joints
    robot_joints_r1, external_axes_r1 = abb_r1.send_and_wait(GetJoints())
    robot_joints_r2, external_axes_r2 = abb_r2.send_and_wait(GetJoints())

    # Print received values
    print('Robot 11: ', robot_joints_r1, external_axes_r1)
    print('Robot 12: ', robot_joints_r2, external_axes_r2)

    # Change robot 1 axis 1
    robot_joints_r1.rax_1 += 30
    string_values_r1 = []
    float_values_r1 = list(robot_joints_r1) + list(external_axes_r1) + [0, 0, 0] + [1000] + [Zone.FINE]

    # Change robot 2 axis 1
    robot_joints_r2.rax_1 += 30
    string_values_r2 = []
    float_values_r2 = list(robot_joints_r2) + list(external_axes_r2) + [0, 0, 0] + [100] + [Zone.FINE]

    # Move with multi move MoveAbsJ
    future_done_r1 = abb_r1.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values_r1, float_values_r1, feedback_level=1))
    future_done_r2 = abb_r2.send(CustomInstruction('r_A042_MultiMove_MoveAbsJ', string_values_r2, float_values_r2, feedback_level=1))

    # Wait for feedback
    done_r1 = future_done_r1.result(timeout=30)
    done_r1 = future_done_r2.result(timeout=30)
    print('MultiMove MoveAbsJ')

    # Deactivate multi move
    string_values, float_values = [], []
    future_done_r1 = abb_r1.send(CustomInstruction('r_A042_ABB_MultiMoveOff', string_values, float_values, feedback_level=1))
    future_done_r2 = abb_r2.send(CustomInstruction('r_A042_ABB_MultiMoveOff', string_values, float_values, feedback_level=1))

    # Wait for feedback
    done_r1 = future_done_r1.result(timeout=5.0)
    done_r1 = future_done_r2.result(timeout=5.0)
    print('MultiMove Off')

    # end of code
    print('Finished')

    abb_r1.close()
    abb_r2.close()

    ros.terminate()
