import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler, ExecuteProcess
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    # Package Directories
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_rrbot_bringup = get_package_share_directory('rrbot_bringup')
    pkg_rrbot_gazebo = get_package_share_directory('rrbot_gazebo')
    pkg_rrbot_description = get_package_share_directory('rrbot_description')
    pkg_rrbot_control = get_package_share_directory('rrbot_control')

    # Launch configuration variables specific to simulation
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    use_rviz = LaunchConfiguration('use_rviz')

    #Declare Launch Arguments    
    declare_world = DeclareLaunchArgument(
          'gz_args', #ign_args
          default_value=[os.path.join(pkg_rrbot_bringup, 'worlds', 'tiny_trr_race.sdf') +
                         ' -v 2 --gui-config ' +
                         os.path.join(pkg_rrbot_bringup, 'config', 'gui.config')
                        , ''],
          description='Ignition Gazebo arguments')
    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        'rviz_config_file',
        default_value=os.path.join(pkg_rrbot_description, 'config', 'robot_visu.rviz'),
        description='Full path to the RVIZ config file to use')  
    declare_use_rviz_cmd = DeclareLaunchArgument(
        'use_rviz',
        default_value='False',
        description='Whether to start RVIZ')

    # Ignition gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),           
    )

    
    #Rviz
    rviz_cmd = Node(
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen')

    # Gazebo Sim - ROS Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{ 
                    'config_file':os.path.join(pkg_rrbot_gazebo, 'config', 'gz_bridge.yaml')
            }],
        remappings=[
            ('/world/empty/model/basic_diff_drive_robot/joint_state', 'diff_drive_joint_states'),
        ],
        output='screen'
    )


    #Spawn Robot
    spawn_rrbot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_rrbot_gazebo, 'launch', 'spawn_rrbot_gz_sim.launch.py'),
        ),
        launch_arguments={'robot_coord_X':'3.5','robot_coord_Y':'-1.65','robot_coord_Z':'0.75','robot_orien_R':'3.1415','robot_orien_Y':'1.56'}.items()
    )     

    #Launch Controllers
    launch_controllers_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_rrbot_control, 'launch', 'rrbot_control.launch.py'),
        ),
        launch_arguments={'use_joint_animation':'True'}.items(),
        # condition=IfCondition(launch_controllers),
    )     

    #Rviz
    rviz_cmd = Node(
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen')
    
    #Static Transforms
    st_tf = Node(
            package='tf2_ros',            
            executable='static_transform_publisher',
            arguments= ["0", "0", "0", "0", "0", "0", "lidar", "rrbot/base_link/lidar"]
        )
    st_tf2 = Node(
            package='tf2_ros',            
            executable='static_transform_publisher',
            arguments= ["0", "0", "0", "0", "0", "0", "front_camera", "rrbot/base_link/front_rgbd_camera"]
        )



    # Create the launch description and populate
    ld = LaunchDescription()


    # Add any conditioned actions
    ld.add_action(declare_world)
    ld.add_action(gazebo)
    ld.add_action(spawn_rrbot)
    ld.add_action(bridge)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(rviz_cmd)
    ld.add_action(launch_controllers_cmd)
    ld.add_action(st_tf)
    ld.add_action(st_tf2)
 

    return ld   
