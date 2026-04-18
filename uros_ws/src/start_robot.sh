#!/bin/bash

echo "?? STARTING ROBOT MAPPING SYSTEM..."

# 1. Set environment variables
export ROS_DOMAIN_ID=0

# (Optional) Make sure your workspaces are sourced
# source /opt/ros/humble/setup.bash
# source ~/PBL5/uros_ws/install/setup.bash

# ==========================================
# SAFE CLEANUP MECHANISM ON CTRL+C
# ==========================================
cleanup() {
    echo ""
    echo "?? Shutting down system safely..."
    # Kill all background processes
    kill $AGENT_PID $TF_PID $LIDAR_PID $SLAM_PID 2>/dev/null
    wait $AGENT_PID $TF_PID $LIDAR_PID $SLAM_PID 2>/dev/null
    echo "? All ROS 2 nodes stopped. USB ports are now released!"
    exit 0
}

# Catch Ctrl+C (SIGINT) and SIGTERM to trigger cleanup
trap cleanup SIGINT SIGTERM

# ==========================================
# START COMPONENTS IN ORDER
# ==========================================

echo "? [1/4] Starting micro-ROS Agent..."
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200 -v6 &
AGENT_PID=$!
sleep 2  # Wait for USB port to be ready

echo "? [2/4] Publishing TF tree (base_link -> laser_frame)..."
ros2 run tf2_ros static_transform_publisher 0.12 0 0.3 0 0 0 base_link laser_frame &
TF_PID=$!
sleep 1

echo "? [3/4] Launching YDLidar..."
ros2 launch ydlidar_ros2_driver ydlidar_launch.py port:=/dev/ydlidar frame_id:=laser_frame &
LIDAR_PID=$!
sleep 3  # Wait for Lidar motor to stabilize

echo "? [4/4] Starting SLAM Toolbox..."
ros2 launch slam_toolbox online_async_launch.py &
SLAM_PID=$!

echo "=========================================="
echo "?? SYSTEM IS READY!"
echo "?? IMPORTANT: Please press the 'EN/RST' button on the ESP32 board now to establish connection!"
echo "?? Press 'Ctrl + C' in this terminal to stop and shut down the entire system."
echo "=========================================="

# Keep script running to listen for Ctrl+C
wait
