import compas_rrc as rrc
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import time

if __name__ == '__main__':

    ros = RosClient("192.168.0.117")
    ros.run()

    robot_11 = rrc.AbbClient(ros, '/robot_1')
    robot_12 = rrc.AbbClient(ros, '/robot_2')

    print('Connected.')
    time.sleep(0.5)

    robot_12.send(rrc.CustomInstruction('r_A067_TPErase',[],[]))
    robot_12.send(rrc.CustomInstruction('r_A067_TPPlot',["Press PLAY to erase"],[]))
    robot_12.send(rrc.CustomInstruction('r_A067_TPPlot',["Press PLAY to erase"],[]))
    robot_12.send(rrc.CustomInstruction('r_A067_TPPlot',["Press PLAY to erase"],[]))
    robot_12.send(rrc.Stop())
    robot_12.send(rrc.CustomInstruction('r_A067_TPErase',[],[]))

    # end of code
    print('Finished')

    time.sleep(5)
    ros.terminate()
    print('Ros terminated')

