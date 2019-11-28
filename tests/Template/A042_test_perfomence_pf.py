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

    # Timer start
    timer_start = time.perf_counter()

    # Dummy
    if off:
        result = abb.send_and_wait(Dummy(feedback_level=1))

    # Dummy
    if on:
        abb.send(Dummy(feedback_level=0))

    # Timer End
    timer_end = time.perf_counter()

    # Print Time
    print(round(timer_end-timer_start,3))

    # Watch read
    if off:
        result = abb.send_and_wait(WatchRead(feedback_level=1))
        print(result)

    # Watch start
    if off:
        result = abb.send_and_wait(WatchStart(feedback_level=1))
        #abb.send(WatchStart(feedback_level=0))


    # watch stop
    if off:
        result = abb.send_and_wait(WatchStop(feedback_level=1))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    # time.sleep(3)
