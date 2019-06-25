#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
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



# jakie tu powinny byc wartosci ????
MIN_FRONT_DISTANCE = 10
MAX_SIDE_SENSORS_DIFFERENCE = 30
SMALL_SIDE_SENSORS_DIFFERENCE = 5

INITIAL_SPEED = 5
MAX_SPEED = 30
SPEED_STEP = 1

TURN_VALUE = 10

speed = 0
angle = 0

def get_speed_and_direction():
    """
            Jezeli roznica miedzy sensorami z lewej i z prawej jest wieksza od MAX_SIDE_SENSORS_DIFFERENCE
            albo SMALL_SIDE_SENSORS_DIFFERENCE to robot zaczyna skrecac (dla MAX_SIDE_SENSORS_DIFFERENCE tez zwalniac)
            jak roznica jest mala, to robot przyspiesza do MAX_SPEED

    """

    global speed
    global angle

    central_front = g_sensor_data['cf']
    central_right = g_sensor_data['cr']
    central_left = g_sensor_data['cl']

    if speed == 0:
        if central_front > MIN_FRONT_DISTANCE:
            speed = INITIAL_SPEED
            angle = 0
        else:
            speed = 0
            angle = 0
    elif central_front < MIN_FRONT_DISTANCE:
        """Stop robot"""
        speed = 0
        angle = 0
    elif abs(central_right-central_left) > MAX_SIDE_SENSORS_DIFFERENCE and central_left < central_right:
        """Turn right,decrease velocity"""
        speed -= SPEED_STEP
        angle -= TURN_VALUE
    elif abs(central_right-central_left) > MAX_SIDE_SENSORS_DIFFERENCE and central_left > central_right:
        """Turn left, decrease velocity"""
        speed -= SPEED_STEP
        angle += TURN_VALUE
    elif abs(central_right-central_left) > SMALL_SIDE_SENSORS_DIFFERENCE and central_left < central_right:
        """ Turn right"""
        speed = speed
        angle -= TURN_VALUE
    elif abs(central_right-central_left) > SMALL_SIDE_SENSORS_DIFFERENCE and central_left > central_right:
        """ Turn left"""
        speed = speed
        angle += TURN_VALUE
    else:
        """Increase velocity"""
        speed = min(speed + SPEED_STEP, MAX_SPEED)
        angle = angle


    # co wpisywac do twist.linear i twist.angualar zeby robot skrecal/przyspieszal/zwalnial itp ???
    return speed, 0, 0, 0, 0, angle


def steer():
    publisher = rospy.Publisher('/cmd/vel', Twist)

    lx, ly, lz, ax, ay, az = get_speed_and_direction()
    twist = Twist()
    twist.linear.x = lx
    twist.linear.y = ly
    twist.linear.z = lz

    twist.angular.x = ax
    twist.angular.y = ay
    twist.angular.z = az

    publisher.publish(twist)



def scanSensors():

    print 'sterr'
    rospy.init_node('driveThrough')
    
    while not rospy.is_shutdown():

        cf_scan_sub = rospy.Subscriber('/laser/scan/cf', Range, cf_callback)
        cb_scan_sub = rospy.Subscriber('/laser/scan/cb', Range, cb_callback)
        cr_scan_sub = rospy.Subscriber('/laser/scan/cr', Range, cr_callback)
        cl_scan_sub = rospy.Subscriber('/laser/scan/cl', Range, cl_callback)
        fr_scan_sub = rospy.Subscriber('/laser/scan/fr', Range, fr_callback)
        fl_scan_sub = rospy.Subscriber('/laser/scan/fl', Range, fl_callback)
        br_scan_sub = rospy.Subscriber('/laser/scan/br', Range, br_callback)
        bl_scan_sub = rospy.Subscriber('/laser/scan/bl', Range, bl_callback)

        steer()
	print 'sterr'

        rospy.spin()


if __name__ == '__main__':
    scanSensors()
