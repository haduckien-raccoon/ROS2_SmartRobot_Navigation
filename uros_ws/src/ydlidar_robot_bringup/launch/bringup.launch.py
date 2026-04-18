from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition
import time
from launch.actions import TimerAction

def generate_launch_description():
    """
    MAIN ENTRY POINT: Kh?i d?ng toàn b? robot.
    - Micro-ROS Agent (ESP32 communication)
    - Robot Description (TF static)
    - Sensors (YDLIDAR)
    - SLAM Toolbox
    - Robot Localization (EKF)
    """
    
    default_robot_launch_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'launch', 'default_robot.launch.py'
    ])
    
    slam_launch_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'launch', 'slam.launch.py'
    ])
    
    ekf_config_path = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'), 'config', 'ekf.yaml'
    ])
    
    slam_launch_delayed = TimerAction(
        period=5.0, 
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(slam_launch_path),
                condition=IfCondition(LaunchConfiguration('use_slam'))
            )
        ]
    )
    

    return LaunchDescription([
        # ============ Arguments ============
        DeclareLaunchArgument(
            'base_serial_port',
            default_value='/dev/ttyUSB0',
            description='ESP32 Serial Port'
        ),
        DeclareLaunchArgument(
            'lidar_port',
            default_value='/dev/ydlidar',  # YDLIDAR
            description='YDLIDAR Serial Port'
        ),

        DeclareLaunchArgument(
            'micro_ros_baudrate',
            default_value='115200',
            description='Micro-ROS baudrate'
        ),

        DeclareLaunchArgument(
            'use_slam',
            default_value='true',
            description='Enable SLAM mapping'
        ),

        DeclareLaunchArgument(
            'use_ekf',
            default_value='true',
            description='Enable EKF odometry fusion'
        ),

        # ============ Launch Sequence ============
        # 1. Robot base (micro_ros_agent + description + sensors)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(default_robot_launch_path),
            launch_arguments={
                'base_serial_port': LaunchConfiguration('base_serial_port'),
                'lidar_port': LaunchConfiguration('lidar_port'),
                'micro_ros_baudrate': LaunchConfiguration('micro_ros_baudrate')
            }.items()
        ),

        # 2. SLAM (depends on /scan from sensors)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch_path),
            condition=IfCondition(LaunchConfiguration('use_slam')),
            launch_arguments={
                'use_slam': LaunchConfiguration('use_slam')
            }.items()
        ),

        # 3. EKF (fuse /odom + /imu ? /odom filtered)
        Node(
            condition=IfCondition(LaunchConfiguration('use_ekf')),
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('odometry/filtered', '/odom')]
        ),
    ])
