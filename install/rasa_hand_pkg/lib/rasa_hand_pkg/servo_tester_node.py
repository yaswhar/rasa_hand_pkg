#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import serial
import threading
import math

class ServoTester(Node):

    def __init__(self):
        super().__init__('servo_tester_node')

        # Declare parameters for serial port configuration
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud = self.get_parameter('baudrate').get_parameter_value().integer_value

        # Open serial port to Arduino Nano
        self.ser = serial.Serial(port, baud, timeout=1)
        self.get_logger().info(f'Opened serial {port}@{baud}')

        # Start background thread to read any incoming lines from Arduino
        threading.Thread(target=self._read_serial, daemon=True).start()

        # Subscribe to the /servo_position topic
        self.create_subscription(
            Float64,
            'servo_position',
            self.position_callback,
            10
        )
        self.get_logger().info('Waiting for Float64 messages on "servo_position"…')

    def _read_serial(self):
        """Continuously read and log lines from the Arduino."""
        while rclpy.ok():
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                self.get_logger().info(f"[Arduino] {line}")

    def position_callback(self, msg: Float64):
        """
        Callback to handle incoming servo position in radians.
        Converts to degrees (0–180), formats a command, and writes to serial.
        """
        radians = msg.data
        # Convert to degrees and constrain between 0 and 180
        degrees = max(0.0, min(180.0, radians * 180.0 / math.pi))  # radians→degrees :contentReference[oaicite:2]{index=2}
        cmd = f"ANGLE:{degrees:.1f}\n"
        self.ser.write(cmd.encode('utf-8'))
        self.get_logger().info(f"→ Sent to Arduino: {cmd.strip()}")

    def destroy_node(self):
        """Ensure serial port is closed when node is destroyed."""
        if self.ser.is_open:
            self.ser.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ServoTester()
    try:
        rclpy.spin(node)   # Keep the node alive, handling callbacks
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()