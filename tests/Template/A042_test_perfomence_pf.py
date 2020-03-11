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

    on = True
    off = False


    # Send_and_wait
    # -->
    # <--
    if off:
        # Read start time
        timer_start = time.perf_counter()

        # Send and wait with no opertation
        result = abb.send_and_wait(Noop(feedback_level=1))

        # Read end time
        timer_end = time.perf_counter()

        # calculate cycle time
        time = round(timer_end-timer_start,3)

        # Print cycletime
        print('Send_and_Wait Cycletime : ', time)

    # Send
    # --> -->
    if on:
        # Read start time python
        python_timer_start = time.perf_counter()

        # Send start for watch on controller
        abb.send(StartWatch())

        # Send stop for watch on controller
        abb.send(StopWatch())

        # Read end time python
        python_timer_end = time.perf_counter()

        # calculate cycle time
        python_time = round(python_timer_end-python_timer_start,3)

        # Print cycletime
        print('Python Send Cycletime : ', python_time)

        # Read time form controller
        irc5_time = abb.send_and_wait(ReadWatch())

        # Print cycletime
        print('IRC5 Send Cycletime : ', irc5_time)

    # Send and wait
    # -->
    # <--
    # -->
    if on:
        # Read start time python
        python_timer_start = time.perf_counter()

        # Send start for watch on controller
        done = abb.send_and_wait(StartWatch())

        # Send stop for watch on controller
        abb.send(StopWatch())

        # Read end time python
        python_timer_end = time.perf_counter()

        # calculate cycle time
        python_time = round(python_timer_end-python_timer_start,3)

        # Print cycletime
        print('Python Send and wait Cycletime : ', python_time)

        # Read time form controller
        irc5_time = abb.send_and_wait(ReadWatch())

        # Print cycletime
        print('IRC5 Send and wait Cycletime : ', irc5_time)

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    # time.sleep(3)
