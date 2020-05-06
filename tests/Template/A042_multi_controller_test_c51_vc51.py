from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb_c51 = AbbClient(ros, '/C51')
    abb_vc51 = AbbClient(ros, '/vC51')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Print Text happy new year
    done_c51 = abb_c51.send_and_wait(PrintText('C51 Robot 1 '))
    done_vc51 = abb_vc51.send_and_wait(PrintText('vC51 Robot 1 '))

    # End of Code
    print('Finished')

    # Close client
    abb_c51.close()
    abb_vc51.close()
    ros.terminate()
