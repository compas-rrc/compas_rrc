from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    # Start ros client
    ros = RosClient()

    # Connect with abb client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # Set tool
    abb.send(CustomInstruction('r_A042_SetTool', ['t_A036_vWG1_Robacta22']))

    # Set workobject
    abb.send(CustomInstruction('r_A042_SetWobj', ['ob_A036_vWAAMTable']))

    # Set joint position
    jointpos_pre_position = [-99.88, 13.69, 38.37, -18.02, 37.41, -85.57]

    # Set robot position
    robpos_weld_start = [202.5, 100, 50, 0.382683432, 0, -0.923879533, 0]
    robpos_weld_90_dec = [199.779, 97.51, 50, 0.27059805, -0.653281482, -0.653281483, -0.27059805]
    robpos_weld_180_dec = [197.5,99.993, 50, 0, 0.923879533, 0.000000001, 0.382683432]
    robpos_weld_270_dec = [200.014, 102.5, 50, 0.27059805, 0.653281483, -0.653281482, 0.27059805]
    robpos_weld_360_dec = [202.5, 100, 50, 0.382683432, 0, -0.923879533, 0]
    robpos_post_position = [237.855110536, 99.999950196, 85.355044039, 0.382683493, 0.000000115, -0.923879507, 0.000000047]

    # Set positon from external axis
    external_axis = [0, 0, 0, 0, 0, 0]

    # Set speed
    speed = [200] # mm/s

    # Set zone
    zone_fine = [Zone.FINE]
    zone_z0 = [Zone.Z0]
    zone_z10 = [Zone.Z10]

    # Set weldspeed
    weldspeed = [10]

    # Set weldjob
    weldjob = [2]

    # Move to pre position
    abb.send(CustomInstruction('r_A042_MoveAbsJ', [], jointpos_pre_position + external_axis + speed + zone_z10))

    # Weld
    abb.send(CustomInstruction('r_A036_ArcLStart', [], robpos_weld_start + external_axis + speed + zone_fine + speed + zone_fine + weldspeed + weldjob))
    abb.send(CustomInstruction('r_A036_ArcC', [], robpos_weld_90_dec + external_axis + robpos_weld_180_dec + external_axis + speed + zone_z0 + weldspeed + weldjob))
    abb.send(CustomInstruction('r_A036_ArcCEnd', [], robpos_weld_270_dec + external_axis + robpos_weld_360_dec + external_axis + speed + zone_fine + weldspeed + weldjob))

    # Move to pre position
    abb.send_and_wait(CustomInstruction('r_A042_MoveL', [], robpos_post_position + external_axis + speed + zone_fine))

    # end of code
    print('Finished')

    abb.close()
    abb.terminate()

    time.sleep(3)
