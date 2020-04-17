from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros,)

    # Run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Switches for Code
    on = True
    off = False

    # Activate soft servo on robot
    # abb.send(CustomInstruction('r_X000_ActSoftRobot',[],[100,100]))

    # wait for user input
    # input("Press any key to continue!")

    # Test GetJointT fuction on master task
    if off:
        done = abb.send_and_wait(CustomInstruction('r_A042_GetJointT',[],[],exec_level=ExecutionLevel.MASTER))
        print(done)

    # Test case send_and_subscribe
    if on:

        # Deactivate soft servo on robot
        # abb.send(CustomInstruction('r_X000_DeactSoftRobot'))
        def get_joint_received(result):
            print(result)

        abb.send_and_subscribe(CustomInstruction('r_A042_CyJobStart',['r_A042_GetJointT'],[1],exec_level=ExecutionLevel.MASTER), get_joint_received)

        # wait for user abort
        input('Press any key to finish!')

        done = abb.send_and_wait(CustomInstruction('r_A042_CyJobEnd',[],[],exec_level=ExecutionLevel.MASTER))
        print('Cyclic job ended', done)

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    ros.terminate()
