#include <chrono>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "morse_interfaces/srv/morse_encode.hpp"

using namespace std::chrono_literals;

class MorseClientNode : public rclcpp::Node
{
private:
    rclcpp::Client<morse_interfaces::srv::MorseEncode>::SharedPtr client_;

public:
    MorseClientNode() : Node("morse_client_node")
    {
        client_ = this->create_client<morse_interfaces::srv::MorseEncode>("/morse_encode");

        while (!client_->wait_for_service(1s))
        {
            if (!rclcpp::ok())
            {
                throw std::runtime_error("Interrupted while waiting for service.");
            }

            RCLCPP_INFO(this->get_logger(), "Waiting for /morse_encode service...");
        }
    }

    void send_text(const std::string &text)
    {
        auto request = std::make_shared<morse_interfaces::srv::MorseEncode::Request>();
        request->text = text;

        auto future = client_->async_send_request(request);

        auto result = rclcpp::spin_until_future_complete(
            this->get_node_base_interface(),
            future);

        if (result != rclcpp::FutureReturnCode::SUCCESS)
        {
            RCLCPP_ERROR(this->get_logger(), "Service call failed.");
            return;
        }

        auto response = future.get();

        if (response->success)
        {
            std::cout << "Text:  " << text << '\n';
            std::cout << "Morse: " << response->morse << '\n';
            std::cout << "Published to /morse_code" << '\n';
        }
        else
        {
            std::cout << "Error: " << response->message << '\n';
        }
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<MorseClientNode>();

    std::string input;

    while (rclcpp::ok())
    {
        std::cout << "Enter text to encode: ";
        std::getline(std::cin, input);

        if (input == "q" || input == "quit" || input == "exit")
        {
            break;
        }

        if (input.empty())
        {
            continue;
        }

        node->send_text(input);
    }

    rclcpp::shutdown();

    return 0;
}