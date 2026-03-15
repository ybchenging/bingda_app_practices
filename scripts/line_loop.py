#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist,Point
from nav_msgs.msg import Odometry


current_position = Point()
target_distance = 0.5#目标距离，单位为米

def getodom(msg):
    global current_position
    current_position = msg.pose.pose.position

def cmd_vel_pub():
    global  target_distance
    rospy.init_node('line_loop')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, getodom)
    rate = rospy.Rate(10)  # 10 Hz
    twist = Twist()
    forword = True
    rospy.loginfo("Starting to move in a line loop...")
    #rospy.sleep(0.1)  # Wait for the first odometry message to be received
    rospy.wait_for_message('/odom', Odometry)

    while not rospy.is_shutdown():

        start_position = Point()
        start_position.x = current_position.x
        start_position.y = current_position.y

        while not rospy.is_shutdown():

            distance = math.sqrt(
                (current_position.x - start_position.x)**2 +
                (current_position.y - start_position.y)**2
            )

            error = target_distance - distance

            if error <= 0:
                twist.linear.x = 0
                pub.publish(twist)
                break

            twist.linear.x = math.sin(error * math.pi)

            if twist.linear.x < 0.05:
                twist.linear.x = 0.05

            if twist.linear.x > 0.2:
                twist.linear.x = 0.2

            if not forword:
                twist.linear.x *= -1

            pub.publish(twist)

            rate.sleep()

        forword = not forword

        
    # while not rospy.is_shutdown():
    #     start_position = Point()
    #     start_position.x = current_position.x
    #     start_position.y = current_position.y
    #     start_position.z = current_position.z
    #     while True:
    #         error = target_distance - ((current_position.x - start_position.x)**2 + (current_position.y - start_position.y)**2)**0.5
    #         if (error > 0):
    #             twist.linear.x = math.sin(error*3.1415926)  # Move forward
    #             if twist.linear.x < 0.05:
    #                 twist.linear.x = 0.05  # Minimum speed to prevent stalling
    #             if twist.linear.x > 0.2:
    #                 twist.linear.x = 0.2  # Maximum speed
    #             if not forword:
    #                 twist.linear.x *= -1.0 # Move backward
    #             else:
    #                 pass
    #             pub.publish(twist)
    #         else:
    #             twist.linear.x = 0.0  # Stop when target distance is reached
    #             pub.publish(twist)
    #             break# Loop until the target distance is reached
    #         rate.sleep()
    #     forword = not forword #forword = bool(1 - forword)  # Toggle direction for the next loop



if __name__ == '__main__':
    try:    
        cmd_vel_pub()   
    except rospy.ROSInterruptException:
        pass
    