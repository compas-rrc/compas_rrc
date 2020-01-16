from compas_rrc import *
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
import re
import time

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # Print Text happy new year
    abb.send(PrintText('I wish you a happy new Year'))

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
