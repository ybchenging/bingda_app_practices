#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry




if __name__ == '__main__':
    rospy.init_node('fro_and_bac')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    twist = Twist()
    twist.linear.x = 0.2  # Linear velocity (m/s)
    rospy.loginfo("Starting to move forward and backward...")
    while not rospy.is_shutdown():
        pub.publish(twist)  # Move forward
        rospy.sleep(2)  # Move forward for 2 seconds
        twist.linear.x = -0.2  # Change to backward velocity
        pub.publish(twist)  # Move backward
        rospy.sleep(2)  # Move backward for 2 seconds
        twist.linear.x = 0.2  # Change back to forward velocity