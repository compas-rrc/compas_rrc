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

    # Test execution roboter and master for channel 1 and 2
    if off:

        # Robot 1
        execution_level = ExecutionLevel.ROBOT

        string_values = ['E-Level Channel 1 Robot']
        float_values = []
        feedback_level = 0
        done = abb_r1.send(CustomInstruction('r_A042_TPWrite', string_values, float_values, feedback_level=feedback_level, exec_level=execution_level))
        done = abb_r1.send_and_wait(WaitTime(1))
        print('Robot Done = ', done)

        # Master 1
        execution_level = ExecutionLevel.MASTER

        string_values = ['E-Level Channel 1 Master']
        float_values = []
        feedback_level = 0
        done = abb_r1.send(CustomInstruction('r_A042_TPWrite', string_values, float_values, feedback_level=feedback_level, exec_level=execution_level))
        done = abb_r1.send_and_wait(WaitTime(1))
        print('Master Done = ', done)

        # Robot 2
        execution_level = ExecutionLevel.ROBOT

        string_values = ['E-Level Channel 2 Robot']
        float_values = []
        feedback_level = 0
        done = abb_r2.send(CustomInstruction('r_A042_TPWrite', string_values, float_values, feedback_level=feedback_level, exec_level=execution_level))
        done = abb_r2.send_and_wait(WaitTime(1))
        print('Robot Done = ', done)

        # Master 2
        execution_level = ExecutionLevel.MASTER

        string_values = ['E-Level Channel 2 Master']
        float_values = []
        feedback_level = 0
        done = abb_r2.send(CustomInstruction('r_A042_TPWrite', string_values, float_values, feedback_level=feedback_level, exec_level=execution_level))
        done = abb_r2.send_and_wait(WaitTime(1))
        print('Master Done = ', done)

    # Test activate cycle job on channel 1
    if on:

        # Start cyclic job
        execution_level = ExecutionLevel.MASTER

        string_values = ['r_A042_CyJobTest']
        float_values = [2.8]
        feedback_level = 0
        done = abb_r1.send_and_wait(CustomInstruction('r_A042_CyJobStart', string_values, float_values, feedback_level=feedback_level, exec_level=execution_level))
        print('Cyclic job started = ', done)

        # User message and input
        input('Press any key to start the print.')

        # End cyclic job
        execution_level = ExecutionLevel.MASTER

        string_values = []
        float_values = []
        feedback_level = 0
        done = abb_r1.send_and_wait(CustomInstruction('r_A042_CyJobEnd', string_values, float_values, feedback_level=feedback_level, exec_level=execution_level))
        print('Cyclic job ended = ', done)

    # end of code
    print('Finished')

    abb_r1.close()
    abb_r2.close()

    ros.terminate()

    time.sleep(3)
