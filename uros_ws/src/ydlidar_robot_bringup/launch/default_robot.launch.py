from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch.substitutions import EqualsSubstitution

def generate_launch_description():
    """
    Kh?i d?ng robot m?c d?nh:
    1. Micro-ROS Agent (ESP32 bridge)
    2. Robot Description (URDF + TF static)
    3. Sensors (YDLIDAR)
    """
    
    description_launch_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'launch', 'description.launch.py'
    ])

    sensors_launch_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'launch', 'sensors.launch.py'
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            'base_serial_port',
            default_value='/dev/ttyUSB0',
            description='ESP32 Serial Port'
        ),
        DeclareLaunchArgument(
            'lidar_port',
            default_value='/dev/ydlidar',
            description='YDLIDAR Port'
        ),

        DeclareLaunchArgument(
            'micro_ros_baudrate',
            default_value='115200',
            description='Micro-ROS baudrate'
        ),

        DeclareLaunchArgument(
            'micro_ros_transport',
            default_value='serial',
            description='Transport: serial | udp4'
        ),

        # Micro-ROS Agent (Serial)
        Node(
            condition=IfCondition(EqualsSubstitution(
                LaunchConfiguration('micro_ros_transport'), 'serial'
            )),
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            output='screen',
            arguments=[
                'serial',
                '--dev', LaunchConfiguration('base_serial_port'),
                '--baudrate', LaunchConfiguration('micro_ros_baudrate')
            ]
        ),

        # Robot Description (URDF + TF publisher)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch_path)
        ),

        # Sensors (YDLIDAR)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sensors_launch_path),
            launch_arguments={
                'port': LaunchConfiguration('lidar_port')
            }.items()
        ),
    ])
