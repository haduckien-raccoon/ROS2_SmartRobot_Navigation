import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

def generate_launch_description():
    """
    Ðon gi?n hóa: Ch? kh?i d?ng YDLIDAR, không có depth camera.
    Lo?i b? logic depthimage_to_laserscan.
    """
    
    laser_sensor_name = os.getenv('YDLIDAR_ROBOT_LASER_SENSOR', 'ydlidar')
    
    laser_launch_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'launch', 'lasers.launch.py'
    ])

    return LaunchDescription([
    	DeclareLaunchArgument(
            'port',
            default_value='/dev/ydlidar',
            description='YDLIDAR port'
        ),
        # ? Ch? launch YDLIDAR (không depth camera)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(laser_launch_path),
            condition=IfCondition(PythonExpression(['"" != "', laser_sensor_name, '"'])),
            launch_arguments={
            	'port': LaunchConfiguration('port'),
                'sensor': laser_sensor_name,
                'frame_id': 'laser_frame',
                'topic_name': 'scan'
            }.items()   
        ),
    ])
