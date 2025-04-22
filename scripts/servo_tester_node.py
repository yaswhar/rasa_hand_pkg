#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
import threading
import time

class ServoTester(Node):

    def __init__(self):
        super().__init__('servo_tester_node')

        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('serial_port').value
        baud = self.get_parameter('baudrate').value

        # Open the serial port
        self.ser = serial.Serial(port, baud, timeout=1)
        self.get_logger().info(f'Opened serial {port}@{baud}')

        # Give Arduino time to reset
        time.sleep(2.0)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        # Thread to echo any Arduino responses
        threading.Thread(target=self._read_serial, daemon=True).start()

        # Sweep settings
        self._angle = 0
        self._step = 5
        self._direction = 1  # +1 = increasing, -1 = decreasing

        # Timer: fire every 20 ms (50 Hz)
        self.create_timer(0.02, self._timer_callback)

        # If you ever want external setpoint control again:
        # self.subscription = self.create_subscription(
        #     Float64, 'servo_position', self.position_callback, 10)

    def _read_serial(self):
        """Echo lines sent back from the Arduino."""
        while rclpy.ok():
            line = self.ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                self.get_logger().info(f"[Arduino] {line}")

    def _timer_callback(self):
        """Called periodically to sweep the servo."""
        # Update angle
        self._angle += self._direction * self._step
        if self._angle >= 180:
            self._angle = 180
            self._direction = -1
        elif self._angle <= 0:
            self._angle = 0
            self._direction = 1

        # Send command
        cmd = f"ANGLE:{self._angle}\n"
        self.ser.write(cmd.encode('utf-8'))
        self.ser.flush()
        self.get_logger().info(f"→ Sent: {cmd.strip()}")

    # In case you keep the subscriber version:
    # def position_callback(self, msg: Float64):
    #     deg = max(0.0, min(180.0, math.degrees(msg.data)))
    #     cmd = f"ANGLE:{deg:.1f}\n"
    #     self.ser.write(cmd.encode('utf-8'))
    #     self.ser.flush()
    #     self.get_logger().info(f"→ Sent: {cmd.strip()}")

    def destroy_node(self):
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