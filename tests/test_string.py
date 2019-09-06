import roslibpy
import time

if __name__ == '__main__':
    ros = roslibpy.Ros('localhost', 9090)

    talker = roslibpy.Topic(ros, '/chatter', 'std_msgs/String')

    def start_talking():
        i = 0
        while ros.is_connected:
            i += 1
            talker.publish(roslibpy.Message({'data': 'M: ' + str(i)}))
            print('Sending message...')
            time.sleep(1)

        talker.unadvertise()
        print('unadvertised')
        time.sleep(1)


    ros.on_ready(start_talking)
    ros.run_forever()
