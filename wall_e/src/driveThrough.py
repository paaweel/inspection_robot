#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Range

g_sensor_data = {}

def cf_callback(msg):
    g_sensor_data['cf'] = msg.range

def cb_callback(msg):
    g_sensor_data['cb'] = msg.range

def cr_callback(msg):
    g_sensor_data['cr'] = msg.range

def cl_callback(msg):
    g_sensor_data['cl'] = msg.range

def fr_callback(msg):
    g_sensor_data['fr'] = msg.range

def fl_callback(msg):
    g_sensor_data['fl'] = msg.range

def br_callback(msg):
    g_sensor_data['br'] = msg.range

def bl_callback(msg):
    g_sensor_data['bl'] = msg.range
        #steer() # czy cos

#def steer():
    #pub = rospy.Publisher(/'cmd_vel', Twist.. )

def scanSensors():
    rospy.init_node('driveThrough')

    cf_scan_sub = rospy.Subscriber('/laser/scan/cf', Range, cf_callback)
    cb_scan_sub = rospy.Subscriber('/laser/scan/cb', Range, cb_callback)
    cr_scan_sub = rospy.Subscriber('/laser/scan/cr', Range, cr_callback)
    cl_scan_sub = rospy.Subscriber('/laser/scan/cl', Range, cl_callback)
    fr_scan_sub = rospy.Subscriber('/laser/scan/fr', Range, fr_callback)
    fl_scan_sub = rospy.Subscriber('/laser/scan/fl', Range, fl_callback)
    br_scan_sub = rospy.Subscriber('/laser/scan/br', Range, br_callback)
    bl_scan_sub = rospy.Subscriber('/laser/scan/bl', Range, bl_callback)

    rospy.spin()


if __name__ == 'main':
    scanSensors()

rospy.spin()
