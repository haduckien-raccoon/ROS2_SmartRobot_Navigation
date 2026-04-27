#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import TransformStamped, Twist, Quaternion
from tf2_ros import TransformBroadcaster
import serial
import math

class ESP32Bridge(Node):
    def __init__(self):
        super().__init__('esp32_bridge')
        self.get_logger().info("=== Khởi tạo ESP32 Odom & IMU Bridge ===")
        
        # --- THÔNG SỐ CƠ HỌC (Khớp với Config.h) ---
        self.cpr = 2400.0             # ENCODER_CPR
        self.wheel_circ = 0.2042      # Chu vi bánh xe (m)
        self.wheelbase = 0.2          # Khoảng cách 2 trục (m) - CẦN ĐO LẠI TRÊN XE THẬT
        
        # --- TRẠNG THÁI ROBOT ---
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.last_ticks = 0
        self.first_run = True
        self.last_time = self.get_clock().now()

        # --- KẾT NỐI SERIAL ---
        serial_port = '/dev/ttyUSB0'  # Đổi thành /dev/ttyACM0 nếu cần
        try:
            self.ser = serial.Serial(serial_port, 115200, timeout=0.1)
            self.get_logger().info(f"Đã kết nối thành công cổng {serial_port}")
        except Exception as e:
            self.get_logger().error(f"LỖI KẾT NỐI SERIAL: {e}")
        
        # --- ROS2 SETUP ---
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data_raw', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Timer chạy ở 20Hz (0.05s) khớp với ESP32
        self.timer = self.create_timer(0.05, self.update_data)

    def update_data(self):
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                
                # 1. Xử lý chuỗi ODOM và IMU
                if line.startswith("ODOM:") and "|IMU:" in line:
                    parts = line.split("|")
                    
                    # Bóc tách Ticks
                    current_ticks = int(parts[0].split(":")[1])
                    
                    # Bóc tách IMU (ax, ay, gz)
                    imu_str = parts[1].split(":")[1]
                    ax, ay, gz = map(float, imu_str.split(","))

                    now = self.get_clock().now()
                    dt = (now - self.last_time).nanoseconds / 1e9

                    # Bỏ qua nhịp đầu tiên để tránh nhảy vọt quãng đường
                    if self.first_run:
                        self.last_ticks = current_ticks
                        self.first_run = False
                        self.get_logger().info(f"Đã nhận tín hiệu đầu tiên! Ticks: {current_ticks}")
                        return

                    # -- TÍNH TOÁN KINEMATICS --
                    delta_ticks = current_ticks - self.last_ticks
                    distance = (delta_ticks / self.cpr) * self.wheel_circ
                    
                    # Tích phân vận tốc góc (Gyro Z) để ra góc quay Yaw (Th)
                    # Lưu ý: Nếu Gyro bị ngược chiều so với ROS, hãy thêm dấu trừ: -gz * dt
                    self.th += gz * dt 
                    
                    # Tính toán x, y
                    self.x += distance * math.cos(self.th)
                    self.y += distance * math.sin(self.th)

                    # -- XUẤT DỮ LIỆU LÊN ROS 2 --
                    self.publish_tf(now)
                    velocity = distance / dt if dt > 0 else 0.0
                    self.publish_odom(now, velocity)
                    self.publish_imu(now, ax, ay, gz)

                    # Cập nhật biến trạng thái
                    self.last_ticks = current_ticks
                    self.last_time = now

                # 2. Xử lý chuỗi GPS (Tạm thời chỉ in ra màn hình)
                elif line.startswith("GPS:"):
                    self.get_logger().info(f"Nhận được {line}")
                    
                # 3. Xử lý chuỗi Cảnh báo
                elif line.startswith("ERR:"):
                    self.get_logger().warn(f"ESP32 BÁO LỖI: {line}")

        except Exception as e:
            # Bắt lỗi ép kiểu hoặc rác Serial
            pass

    def publish_tf(self, now):
        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation = self.yaw_to_quat(self.th)
        self.tf_broadcaster.send_transform(t)

    def publish_odom(self, now, velocity):
        msg = Odometry()
        msg.header.stamp = now.to_msg()
        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_link'
        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.orientation = self.yaw_to_quat(self.th)
        msg.twist.twist.linear.x = velocity
        msg.twist.twist.angular.z = 0.0 # Tạm thời không cần vì đã có IMU
        self.odom_pub.publish(msg)

    def publish_imu(self, now, ax, ay, gz):
        msg = Imu()
        msg.header.stamp = now.to_msg()
        msg.header.frame_id = 'base_link' # Gắn trực tiếp vào base_link
        # Gia tốc tuyến tính (m/s^2)
        msg.linear_acceleration.x = ax
        msg.linear_acceleration.y = ay
        msg.linear_acceleration.z = 9.81 # Trọng lực giả định
        # Vận tốc góc (rad/s)
        msg.angular_velocity.x = 0.0
        msg.angular_velocity.y = 0.0
        msg.angular_velocity.z = gz
        self.imu_pub.publish(msg)

    def yaw_to_quat(self, yaw):
        return Quaternion(x=0.0, y=0.0, z=math.sin(yaw/2), w=math.cos(yaw/2))

def main(args=None):
    rclpy.init(args=args)
    node = ESP32Bridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Đang đóng kết nối...")
    finally:
        if hasattr(node, 'ser') and node.ser.is_open:
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
