from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # Get URDF file path
    urdf_file = PathJoinSubstitution([
        FindPackageShare('ydlidar_robot_bringup'),
        'urdf',
        'robot.urdf.xacro'
    ])

    # Use xacro to process URDF file
    robot_description_content = Command([
        'xacro ',
        urdf_file
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            'namespace',
            default_value='/',
            description='Robot namespace'
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description_content,
                'frame_prefix': '',
            }]
        ),

        # Optional: Joint State Publisher GUI (d? test)
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
    ])
