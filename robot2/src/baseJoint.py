#!/usr/bin/env python

import rospy
import operator
from std_msgs.msg import Float64MultiArray

def steer():
    rospy.init_node('trajectory_ex')
    pub = rospy.Publisher('/robot2_legs_controller/command', Float64MultiArray, queue_size = 10)
    array = [0 for i in range(8)]
    rate = rospy.Rate(20)
    keyPresses = 0
    while not rospy.is_shutdown():
        while keyPresses < 8:
            inp = input("Enter new pos = ")
            if inp > 5:
                keyPresses = keyPresses + 1
            else:
                array[6] = inp
                msg = Float64MultiArray(data=array)
                pub.publish(msg)
                print msg

        print "zbazowane"
        print msg
    rate.sleep()

if __name__ == '__main__':
    try:
        steer()
    except rospy.ROSInterruptException:
        pass
