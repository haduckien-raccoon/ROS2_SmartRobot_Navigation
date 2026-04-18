from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.substitutions import EqualsSubstitution

def generate_launch_description():
    """
    Ch? support YDLIDAR (lo?i b? rplidar, ldlidar, v.v...)
    """
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'sensor',
            default_value='ydlidar',
            description='Sensor type'
        ),

        DeclareLaunchArgument(
            'frame_id',
            default_value='laser_frame',
            description='Laser frame ID'
        ),

        DeclareLaunchArgument(
            'topic_name',
            default_value='scan',
            description='Laser scan topic'
        ),

        DeclareLaunchArgument(
            'port',
            default_value='/dev/ydlidar',
            description='Laser serial port'
        ),

        # YDLIDAR Node
        Node(
            condition=IfCondition(EqualsSubstitution(
                LaunchConfiguration('sensor'), 'ydlidar'
            )),
            package='ydlidar_ros2_driver',
            executable='ydlidar_ros2_driver_node',
            name='ydlidar_ros2_driver_node',
            output='screen',
            emulate_tty=True,
            remappings=[('scan', LaunchConfiguration('topic_name'))],
            parameters=[{
                'port': LaunchConfiguration('port'),
                'frame_id': LaunchConfiguration('frame_id'),
                'lidar_type': 1,
                'device_type': 6,
                'sample_rate': 5,
                'baudrate': 128000,
                'angle_max': 180.0,
                'angle_min': -180.0,
                'range_max': 10.0,
                'range_min': 0.12,
                'frequency': 5.0,
            }]
        ),
    ])
