from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import time
import roslibpy

ros = RosClient('192.168.125.117')
abb = AbbClient(ros,namespace='robot_1') # robot_1 namespace for compas_rrc commandss
abb.run()
ros.run()
print('Connected.')

# Initialize, tools, wobj,  external axis

robot_joints, external_axes = abb.send_and_wait(GetJoints())
abb.send(SetTool('t_A053_RollerV2'))
print('Tool set')

abb.send(CustomInstruction('r_A053_RunEGM'))
print('Switching to EGM')

time.sleep(5)
# set IO

print('Closing EGM connection')
# abb.send(CustomInstruction('r_A053_KillEGM'))

robot_joints, external_axes = abb.send_and_wait(GetJoints())
print('Robot joint values via RRC)', robot_joints)

# Close client
abb.close()


