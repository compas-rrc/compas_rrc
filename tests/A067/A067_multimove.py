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
    robot11_joints, external11_axes = robot_11.send_and_wait(rrc.GetJoints())
    robot12_joints, external12_axes = robot_12.send_and_wait(rrc.GetJoints())

    # Print received values
    print(robot11_joints, external11_axes)
    print(robot12_joints, external12_axes)

    # Print confirm message to TP
    robot_12.send(rrc.PrintText('Press PLAY to execute'))
    robot_11.send(rrc.Stop())
    robot_12.send(rrc.Stop())
    
    # Set multi move tasklist
    string_values, float_values = ['T_ROB11', 'T_ROB12'], []
    done_r1 = robot_11.send_and_wait(rrc.CustomInstruction('r_A042_ABB_SetMultiMoveTasks', string_values, float_values))

    # Activate multi move
    string_values, float_values = [], []
    future_done_r11 = robot_11.send(rrc.CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))
    future_done_r12 = robot_12.send(rrc.CustomInstruction('r_A042_ABB_MultiMoveOn', string_values, float_values, feedback_level=1))
 
    # Wait for feedback
    done_r11 = future_done_r11.result()
    done_r12 = future_done_r12.result()
    print('MultiMove On')

    robot_12.send(rrc.PrintText('Press PLAY to continue'))
    robot_11.send(rrc.Stop())
    robot_12.send(rrc.Stop())

    # Send a list of points
    points = [
        [[-6.91, -64.44, 27.17, -7.88, 7.84, -11.02], [23000, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.35, -61.24, 25.53, -6.28, 6.26, -12.35], [23400, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.53, -58.65, 24.09, -5.96, 5.09,  40.00], [24000, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.66, -55.73, 22.36, -6.19,  3.9, -12.28], [23400, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        [[-7.75, -52.56, 20.34, -7.18, 2.75, -11.24], [23000, -3756.72, -3716.9, 0.0, 0.0, 0.0]],
        ]

    for robot12_joints, external12_axes in points:
        external11_axes[0] = external12_axes[0]
        float_values_r11 = list(robot11_joints) + list(external11_axes) + [0, 0, 0] + [500] + [rrc.Zone.Z5]
        float_values_r12 = list(robot12_joints) + list(external12_axes) + [0, 0, 0] + [500] + [rrc.Zone.Z5]
        print ("sent to robot11:", robot11_joints, external11_axes)
        print ("sent to robot12:", robot12_joints, external12_axes)
        # Move with multi move MoveAbsJ
        robot_11.send(rrc.CustomInstruction('r_A042_MultiMove_MoveAbsJ', [], float_values_r11, feedback_level=1))
        robot_12.send(rrc.CustomInstruction('r_A042_MultiMove_MoveAbsJ', [], float_values_r12, feedback_level=1))


    # robot_12.send(rrc.PrintText('Completed'))


    # Deactivate multi move
    future_done_r11 = robot_11.send(rrc.CustomInstruction('r_A042_ABB_MultiMoveOff', [], [], feedback_level=1))
    future_done_r12 = robot_12.send(rrc.CustomInstruction('r_A042_ABB_MultiMoveOff', [], [], feedback_level=1))

    # Wait for feedback
    done_r11 = future_done_r11.result()
    done_r12 = future_done_r12.result()
    print('MultiMove Off')

    # end of code
    print('Finished')

    time.sleep(3)
    ros.terminate()
    time.sleep(3)
    print('ros terminated')
