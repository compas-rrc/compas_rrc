from abb_a042_base_lib import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    ros = RosClient()

    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # set speed
    speed = 500

    # set tool
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['t_A014_T1LaserSensor'], feedback_level=1))
    print("Set Tool:", result['instruction'])

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['ob_A014_TestBase'], feedback_level=1))
    print("Set Workobject:", result['instruction'])

    x = 250
    y = 340
    z = 120
    q1 = 0
    q2 = -0.707
    q3 = 0.707
    q4 = 0
    ex = 28000
    ey = -3700
    ez = -2800

    # initalizie counter

    step = 10
    start = 250
    end = 300
    searchposition = start

    # measure loop
    while searchposition <= end:

        # create ropot data
        x = searchposition
        rob_point = Frame.from_quaternion([q1, q2, q3, q4], [x, y, z])
        ext_axis = [ex, ey, ez]

        # move to scan position
        abb.send(MoveL(rob_point, ext_axis, speed, Zone.FINE))

        # scan
        result = abb.send_and_wait(ProjectInstruction('r_A014_Scan', feedback_level=1))
        distance = result['float_values'][0]
        feedback_info = result['string_values'][0]

        # print robot feedback
        print("")
        print("Distance:", distance)
        print("Measure feedback:", feedback_info)
        print("Searchpoint:",searchposition)

        # update searchpostion
        searchposition += step

    # end of code
    print("")
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
