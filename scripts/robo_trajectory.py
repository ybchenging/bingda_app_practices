#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist,Point

path_pub  = rospy.Publisher('/robo_trajectory', Path, queue_size=10)
trajectory = Path()

def getodom(msg):
    global trajectory
    global path_pub
    this_pose_stamped = PoseStamped()
    this_pose_stamped.pose.position = msg.pose.pose.position
    this_pose_stamped.pose.orientation = msg.pose.pose.orientation
    this_pose_stamped.header.frame_id = msg.header.frame_id
    this_pose_stamped.header.stamp = msg.header.stamp

    trajectory.header.frame_id = this_pose_stamped.header.frame_id
    trajectory.header.stamp = this_pose_stamped.header.stamp
    trajectory.poses.append(this_pose_stamped)
    path_pub.publish(trajectory)




def listneer():
    rospy.init_node('robo_trajectory')
    #pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    odom_sub = rospy.Subscriber('/odom', Odometry, getodom)
    rospy.loginfo("Starting to record robot trajectory...")
    rospy.spin()






if __name__ == '__main__':
    try:
        listneer()
    except rospy.ROSInterruptException:
        pass