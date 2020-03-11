from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient('192.168.125.42')

    # Create ABB Client
    abb_c51 = AbbClient(ros, '/c51')
    abb_vc51 = AbbClient(ros, '/vc51')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Print Text happy new year
    abb_c51.send(PrintText('IRB120 Real Controller '))
    abb_vc51.send(PrintText('IRB120 Virtual Controller '))

    # End of Code
    print('Finished')

    # Close client
    abb_c51.close()
    abb_vc51.close()
    ros.terminate()
