#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import serial
import threading
import math
import time

class ServoTester(Node):

    def __init__(self):
        super().__init__('servo_tester_node')

        # Declare parameters
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud = self.get_parameter('baudrate').get_parameter_value().integer_value

        # Open the serial port
        self.ser = serial.Serial(port, baud, timeout=1)
        self.get_logger().info(f'Opened serial {port}@{baud}')

        # Wait ~2s for Arduino auto‑reset & bootloader
        time.sleep(2.0)
        # Flush any spurious data
        self.ser.reset_input_buffer()

        # Start a thread to print any Arduino responses
        threading.Thread(target=self._read_serial, daemon=True).start()

        # Create and **store** the subscription so it isn't GC'd
        self.subscription = self.create_subscription(
            Float64,
            'servo_position',
            self.position_callback,
            10
        )
        self.get_logger().info('Subscribed to /servo_position; waiting for messages…')

    def _read_serial(self):
        """Continuously read and log lines from the Arduino."""
        while rclpy.ok():
            line = self.ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                self.get_logger().info(f"[Arduino] {line}")

    def position_callback(self, msg: Float64):
        """Convert incoming radians → degrees, send angle command."""
        radians = msg.data
        degrees = max(0.0, min(180.0, radians * 180.0 / math.pi))
        cmd = f"ANGLE:{degrees:.1f}\n"
        self.ser.write(cmd.encode('utf-8'))
        self.ser.flush()  # ensure it goes out immediately
        self.get_logger().info(f"→ Sent: {cmd.strip()}")

    def destroy_node(self):
        """Clean up serial on shutdown."""
        try:
            if self.ser.is_open:
                self.ser.close()
        except Exception:
            pass
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ServoTester()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()