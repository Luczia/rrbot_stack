#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import rclpy
from gazebo_msgs.srv import SpawnEntity

def main(args=None):
    # Get input arguments from user
    argv = sys.argv[1:] 
    rclpy.init(args=args)
    node = rclpy.create_node('entity_spawner')
    cli = node.create_client(SpawnEntity, '/spawn_entity')
   

    req = SpawnEntity.Request()
    req.name = argv[0]
    req.xml = argv[1]
    req.robot_namespace = argv[2]
    req.reference_frame = argv[3]
   
    req.initial_pose.position.x = float(argv[4])
    req.initial_pose.position.y = float(argv[5])
    req.initial_pose.position.z = float(argv[6])
    req.initial_pose.orientation.w = float(argv[7])
    req.initial_pose.orientation.x = float(argv[8])
    req.initial_pose.orientation.y = float(argv[9])
    req.initial_pose.orientation.z = float(argv[10])

    while not cli.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('service not available, waiting again...')

    future = cli.call_async(req)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info(
            'Result ' + str(future.result().success) + " " + future.result().status_message)
    else:
        node.get_logger().info('Service call failed %r' % (future.exception(),))

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
