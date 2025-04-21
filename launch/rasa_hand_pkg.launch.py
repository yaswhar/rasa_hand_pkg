from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rasa_hand_pkg',
            executable='servo_tester_node.py',
            name='servo_tester_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'baudrate': 115200
            }]
        ),
    ])