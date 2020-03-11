from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    abb.send(CustomInstruction('r_A053_RunEGM'))
    print('Switching to EGM')

    # User message and input
    input('Robot start position reached, press any key to start the print.')

    abb.send(CustomInstruction('r_A053_StopEGM', exec_level=ExecutionLevel.MASTER))
    print('Switching to EGM')

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
