from abb_a042_base_lib import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':
    with open('code.txt', 'r') as f:
        lines = f.readlines()
    regex = re.compile(r'\[(.+?)\],\[(.+?)\],\[(.+?)\],(\d+),(.+)')

    print('Read %d lines of code, ready to connect.' % len(lines))

    instructions = []
    for line in lines:
        m = regex.search(line)
        point = list(map(float, m.group(1).split(',')))
        orientation = list(map(float, m.group(2).split(',')))
        ext_axes = list(map(float, m.group(3).split(',')))
        speed = int(m.group(4))
        zone = m.group(5).split('.')[0] + '.' + m.group(5).split('.')[1].upper()
        zone = eval(zone)
        # print('Point: ', point)
        # print('Orient: ', orientation)
        # print('Ext Ax: ', ext_axes)
        # print('Speed: ', speed)
        # print('Zone: ', zone)
        target_frame = Frame.from_quaternion(orientation, point)
        instruction = MoveL(target_frame, ext_axes, speed, zone)
        instructions.append(instruction)

    print('Correctly parsed %d instructions.' % len(instructions))

    ros = RosClient()

    abb = AbbClient(ros)
    abb.run()
    print('Connected.')
    instructions = instructions[0:10000]

    for instruction in instructions:
        print(instruction)
        abb.send(instruction)

    last = instructions[-1]
    last.feedback_level = MotionFeedback.DONE
    print('Waiting for last instruction to complete...')
    abb.send_and_wait(last)

    # abb.send_and_wait(MoveAbsJ([90, 45, 0, 1, 10, 20], [28000, -6500, -4500], 2000, Zone.FINE, feedback_level=1))

    # abb.send(ProjectInstruction('r_A032_AP1_SpeedUpdate', ['First test'], [10.5]))

    # abb.send(MoveAbsJ([90, 45, 0, 1, 10, 20], [28000, -6500, -3500], 2000, Zone.Z200))
    # abb.send(MoveAbsJ([90, 45, 0, 1, 10, 20], [28000, -6000, -3500], 2000, Zone.Z200))
    # abb.send(MoveAbsJ([90, 45, 0, 1, 10, 20], [28000, -7000, -3500], 2000, Zone.Z200))
    # abb.send(MoveAbsJ([90, 45, 0, 1, 10, 20], [28000, -6500, -3500], 2000, Zone.Z200))
    # abb.send_and_wait(MoveAbsJ([90, 45, 0, 1, 10, 20], [28000, -6500, -4500], 2000, Zone.FINE, feedback_level=1))

    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
