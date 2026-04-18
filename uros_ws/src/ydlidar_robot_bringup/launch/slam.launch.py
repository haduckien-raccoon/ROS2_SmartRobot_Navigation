from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
    """
    Kh?i d?ng SLAM Toolbox (online_async mode).
    """
    
    slam_config_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'config', 'mapper_params_online_async.yaml'
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_slam',
            default_value='true',
            description='Enable SLAM mapping'
        ),

        Node(
            condition=IfCondition(LaunchConfiguration('use_slam')),
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox_node',
            output='screen',
            parameters=[slam_config_path],
            remappings=[
                ('scan', '/scan'),
                ('map', '/map'),
                ('tf', '/tf'),
                ('tf_static', '/tf_static')
            ]
        ),
    ])
