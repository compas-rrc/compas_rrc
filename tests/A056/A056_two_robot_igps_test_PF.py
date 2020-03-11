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
    if off:

        # Get frame
        frame, external_axes = abb_r1.send_and_wait(GetRobtarget())

        # Print received values
        print(frame, external_axes)

        # Change any value and move to new position
        frame.point[2] += 50
        done = abb_r1.send_and_wait(MoveToRobtarget(frame, external_axes, 100, Zone.FINE))

        # measage done
        print('Robot 1 Finished')

    # iGPS test robot 1
    if on:

        # Connect with iGPS Server
        string_values = ['Robot11']
        float_values = []
        feedback_level = 0
        abb_r1.send(CustomInstruction('r_A042_iGPS_Connect', string_values, float_values, feedback_level=feedback_level))

        # Set Tool
        abb_r1.send(SetTool('tT11TimGr1'))

        # Set Work Object
        abb_r1.send(SetWorkObject('igps_wobj0'))

        # Set iGPS tool
        string_values = ['tT11TimGr1']
        float_values = []
        feedback_level = 0
        abb_r1.send(CustomInstruction('r_A042_iGPS_SetTool', string_values, float_values, feedback_level=feedback_level))

        # Set iGPS work object
        string_values = ['wobj0']
        float_values = []
        feedback_level = 0
        abb_r1.send(CustomInstruction('r_A042_iGPS_SetWobj', string_values, float_values, feedback_level=feedback_level))

        # Get frame
        frame, external_axes = abb_r1.send_and_wait(GetRobtarget())
        print('GetRobtarget Result = ', frame.point, frame.quaternion , external_axes)

        # iGPS move and correct
        string_values = []
        float_values = list(frame.point) + list(frame.quaternion) + list(external_axes) + [0.0, 0.0, 0.0] + [100.0] + [Zone.FINE]
        feedback_level = 1
        done = abb_r1.send_and_wait(CustomInstruction('r_A042_iGPS_MoveLAndCorrect', string_values, float_values, feedback_level=feedback_level))

    # end of code
    print('Finished')

    abb_r1.close()
    abb_r2.close()

    ros.terminate()

    time.sleep(3)
