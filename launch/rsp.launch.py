import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('rover_bot'))
    xacro_file = os.path.join(pkg_path,'urdf','my_robot_core.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    rviz_path = pkg_path+'/rviz/my_robot.rviz'


    # World Config
    world_file_name = 'my_world.world'
    world_path = os.path.join(pkg_path, 'worlds', world_file_name)

    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': True}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Launch rviz2
    node_rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=['-d', str(rviz_path)]
    )

    # Launch a joint_state_publisher_gui node
    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

        # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'world': world_path}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'rover_bot'],
                        output='screen')



    # Launch!
    return LaunchDescription([

        node_rviz2,
        node_robot_state_publisher,
        # node_joint_state_publisher_gui,
        gazebo,
        spawn_entity,
        
    ])