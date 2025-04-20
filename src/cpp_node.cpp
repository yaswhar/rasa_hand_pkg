#include <rclcpp/rclcpp.hpp>
// Include your header file to use it
#include "rasa_hand_pkg/cpp_header.hpp"
int main(int argc, char **argv)
{
// Initiate ROS communications
    rclcpp::init(argc, argv);
// Instantiate the node
    auto node = std::make_shared<rclcpp::Node>("my_node_name");
// Make the node spin
    rclcpp::spin(node);
// Shutdown ROS communications
    rclcpp::shutdown();
    return 0;
}