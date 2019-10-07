from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':
    # with open('tests/code.txt', 'r') as f:
    with open('tests/20190925beam print.txt', 'r') as f:
        lines = f.readlines()
    regex = re.compile(r'\[(.+?)\],\[(.+?)\],\[(.+?)\],(\d+),(.+)')
    # lines = lines[0:10]
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

    # set tool
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetTool', ['t_A032_PrintNozzle2'], feedback_level=1))
    print("Set Tool:", result['instruction'])

    # set workobject
    result = abb.send_and_wait(ProjectInstruction('r_A042_SetWorkobject', ['ob_A032_Pal1'], feedback_level=1))
    print("Set Workobject:", result['instruction'])

    # instructions = instructions[0:1000]
    # instructions = instructions[0:3000]
    # instructions = instructions[0:70000]
    instructions = instructions[0:-1]

    for instruction in instructions:
        print(instruction)
        abb.send(instruction)

    # for i in range(100000):
    #     print(instruction)
    #     instruction = ProjectInstruction('r_A042_Dummy', [], [])
    #     instruction = instructions
    #     abb.send(instruction)
    #     if instruction.sequence_id % 300 == 0:
    #         print(instruction)

    last = instructions[-1]
    last.feedback_level = MotionFeedback.DONE

    print('Waiting for last instruction to complete...')
    abb.send_and_wait(last)

    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
