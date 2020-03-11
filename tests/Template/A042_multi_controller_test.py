from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # Print Text happy new year
    abb.send(PrintText('IRB120 Real Controller '))

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
