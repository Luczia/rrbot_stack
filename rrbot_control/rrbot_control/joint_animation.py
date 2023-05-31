#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

import math
from random import uniform

class JointTrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('joint_animation_publisher')
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
           

    def timer_callback(self):
        self.jt = JointTrajectory()
        self.jt.header.frame_id = "world"
        self.jt.joint_names.append("hip_pivot_right")
        self.jt.joint_names.append("hip_pivot_left")     
        self.jt.joint_names.append("knee_pivot_right")
        self.jt.joint_names.append("knee_pivot_left")    
        # self.sit_down_pos()
        self.traj_pub()
        self.get_logger().info('Publishing \n')
        self.i += 1

    def sit_down_pos(self):
        p = JointTrajectoryPoint()
        p.positions.append(1.45)
        p.positions.append(1.45)
        p.positions.append(0.5)
        p.positions.append(0.5)
        self.jt.points.append(p)
        self.jt.points[0].time_from_start = rclpy.duration.Duration(seconds=0.1).to_msg()
        self.publisher_.publish(self.jt)

    
    def traj_pub(self):
        #self.jt.header.stamp = self.get_clock().now().to_msg()    #TO FIX, don't know why its fails to run on Gazebo
        
        n = 1   #number of points in the trajectory
        dt = 1   #delta time between two points
        rps = 0.5 #radians/sec        
        for i in range (n):
            p = JointTrajectoryPoint()
            theta = rps*2.0*math.pi*i*dt
            x1 = uniform(-rps,rps)#-0.5*math.sin(2*theta)
            x2 = uniform(-rps,rps)# 0.5*math.sin(1*theta)

            p.positions.append(x1)
            p.positions.append(x2)
            p.positions.append(x1)
            p.positions.append(x2)
            self.jt.points.append(p)

            # set duration
            self.jt.points[i].time_from_start = rclpy.duration.Duration(seconds=0.1).to_msg()
            # self.get_logger().info('test: angles[%d][%f, %f]' % (n,x1,x2))
        self.publisher_.publish(self.jt)



def main(args=None):
    rclpy.init(args=args)

    joint_traj_pub = JointTrajectoryPublisher()

    rclpy.spin(joint_traj_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    joint_traj_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

