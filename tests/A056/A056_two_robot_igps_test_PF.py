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

        # Get frame
        frame, external_axes = abb_r1.send_and_wait(GetRobtarget())

        # Print received values
        print(frame, external_axes)

        # Connect with iGPS Server
        abb_r1.send(CustomInstruction('r_A042_iGPS_Connect',['Robot11'],[]))

    # end of code
    print('Finished')

    abb_r1.close()
    abb_r2.close()

    ros.terminate()

    time.sleep(3)
