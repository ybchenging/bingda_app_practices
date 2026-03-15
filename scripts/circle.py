#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    rospy.init_node('circle')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    twist = Twist()
    twist.linear.x = 0.2  # Linear velocity (m/s)
    twist.angular.z = 0.5  # Angular velocity (rad/s)
    rospy.loginfo("Starting to move in a circle...")
    while not rospy.is_shutdown():
        pub.publish(twist)
        rate.sleep()