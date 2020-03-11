from compas_rrc import *
from compas_fab.backends.ros import RosClient

if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient('192.168.125.42')

    # Create ABB Client
    abb_c51 = AbbClient(ros, '/c51')
    abb_vc11_r11 = AbbClient(ros, '/vc11_r11')
    abb_vc11_r12 = AbbClient(ros, '/vc11_r12')

    # run the eventloop on python to connect with ros
    ros.run()
    print('Connected.')

    # Print Text happy new year
    abb_c51.send(PrintText('C51 Robot 1 '))
    abb_vc11_r11.send_and_wait(PrintText('vC11 Robot 11 '))
    input("Any key")
    abb_vc11_r12.send(PrintText('vC11_Robot 12 '))

    # End of Code
    print('Finished')

    # Close client
    abb_c51.close()
    abb_vc11_r11.close()
    abb_vc11_r12.close()
    ros.terminate()
