from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    # open path file
    with open('tests/A032/20190925beam print.txt', 'r') as f:
        lines = f.readlines()

    # ?
    regex = re.compile(r'\[(.+?)\],\[(.+?)\],\[(.+?)\],(\d+),(.+)')

    # limit number of lines
    lines = lines[0:90]

    # user information
    print('Read %d lines of code, ready to connect.' % len(lines))

    # genereate path instructions for robot
    path_instructions = []
    for line in lines:
        m = regex.search(line)
        point = list(map(float, m.group(1).split(',')))
        orientation = list(map(float, m.group(2).split(',')))
        ext_axes = list(map(float, m.group(3).split(',')))
        speed = int(m.group(4))
        zone = m.group(5).split('.')[0] + '.' + m.group(5).split('.')[1].upper()
        zone = eval(zone)
        target_frame = Frame.from_quaternion(orientation, point)
        instruction = MoveL(target_frame, ext_axes, speed, zone)
        path_instructions.append(instruction)

    print('Correctly parsed %d instructions.' % len(path_instructions))

    # create a ros client
    ros = RosClient()

    # connect with compas rrc ros
    abb = AbbClient(ros)
    abb.run()
    print('Compas RRC Ros = Connected.')

    # set tool
    abb.send(SetTool('t_A032_PrintNozzle2'))

    # set workobject
    abb.send(SetWobj('ob_A032_Pal1'))

    path_instructions = path_instructions[0:-1]
    for path_instruction in path_instructions:
        print(path_instruction)
        abb.send(path_instruction)

    last = path_instructions[-1]
    last.feedback_level = MotionFeedback.DONE

    print('Waiting for last instruction to complete...')
    abb.send_and_wait(last)

    print('Finished')


    # close compas rrc connection
    abb.close()
    abb.terminate()

    time.sleep(3)
