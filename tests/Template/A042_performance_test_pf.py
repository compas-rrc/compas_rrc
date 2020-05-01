from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient

import re
import time

if __name__ == '__main__':

    ros = RosClient()

    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # ==============================================================================
    # Performance test
    # -> Max Data Test
    # ==============================================================================

    # Instrucion name (32 chars)
    instruction = 'r_A042_PerfoooormanceTestMaxData'

    # Maximal string length (Protocoll v1 5x and v2 8x 80 chars)
    string_1 = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    string_2 = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
    string_3 = 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'
    string_4 = 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'
    string_5 = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    string_6 = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    string_7 = 'gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg'
    string_8 = 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    string_values = [string_1, string_2, string_3, string_4, string_5, string_6, string_7, string_8]
    string_values = [string_1, string_2, string_3, string_4, string_5]

    # Maximal values (Protocoll v1 30 and v2 36 floats)
    float_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0]
    float_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0]

    # Read start time
    timer_start = time.perf_counter()

    # Send and wait with maximal data custom instruction
    result = abb.send_and_wait(CustomInstruction(instruction, string_values, float_values,feedback_level=FeedbackLevel.DONE, exec_level= ExecutionLevel.ROBOT))

    # Read end time
    timer_end = time.perf_counter()

    # calculate cycle time
    send_and_wait_time = round(timer_end-timer_start,3)

    # Print cycletime
    print('send_and_wait with max data time : ', send_and_wait_time)

    # ==============================================================================
    # Performance test
    # -> Min Data Test
    # ==============================================================================

    # Instrucion name (8 chars)
    instruction = 'r_A042_P'

    # Minimal string length (Protocoll v1 and v2 0 char)
    string_values = []

    # Minimal values (Protocoll v1 and v2 1 floats)
    float_values = [1.0]

    # Read start time
    timer_start = time.perf_counter()

    # Send and wait with maximal data custom instruction
    result = abb.send_and_wait(CustomInstruction(instruction, string_values, float_values,feedback_level=FeedbackLevel.DONE, exec_level= ExecutionLevel.ROBOT))

    # Read end time
    timer_end = time.perf_counter()

    # calculate cycle time
    send_and_wait_time = round(timer_end-timer_start,3)

    # Print cycletime
    print('send_and_wait with min data time : ', send_and_wait_time)

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    # time.sleep(3)
