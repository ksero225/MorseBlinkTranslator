#include <cctype>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "morse_interfaces/srv/morse_encode.hpp"

class MorseEncoderServiceNode : public rclcpp::Node
{
private:
    rclcpp::Service<morse_interfaces::srv::MorseEncode>::SharedPtr service_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr morse_publisher_;

    const std::unordered_map<char, std::string> morse_code_ = {
        {'A', ".-"}, {'B', "-..."}, {'C', "-.-."}, {'D', "-.."}, {'E', "."}, {'F', "..-."}, {'G', "--."}, {'H', "...."}, {'I', ".."}, {'J', ".---"}, {'K', "-.-"}, {'L', ".-.."}, {'M', "--"}, {'N', "-."}, {'O', "---"}, {'P', ".--."}, {'Q', "--.-"}, {'R', ".-."}, {'S', "..."}, {'T', "-"}, {'U', "..-"}, {'V', "...-"}, {'W', ".--"}, {'X', "-..-"}, {'Y', "-.--"}, {'Z', "--.."},

        {'0', "-----"},
        {'1', ".----"},
        {'2', "..---"},
        {'3', "...--"},
        {'4', "....-"},
        {'5', "....."},
        {'6', "-...."},
        {'7', "--..."},
        {'8', "---.."},
        {'9', "----."},

        {'.', ".-.-.-"},
        {',', "--..--"},
        {'?', "..--.."},
        {'!', "-.-.--"},
        {'-', "-....-"},
        {':', "---..."},
        {'/', "-..-."}};

public:
    MorseEncoderServiceNode() : Node("morse_encoder_service_node")
    {
        morse_publisher_ = this->create_publisher<std_msgs::msg::String>("/morse_code", 10);

        service_ = this->create_service<morse_interfaces::srv::MorseEncode>(
            "/morse_encode",
            std::bind(
                &MorseEncoderServiceNode::encode_callback,
                this,
                std::placeholders::_1,
                std::placeholders::_2));

        RCLCPP_INFO(this->get_logger(), "Morse encoder service started.");
        RCLCPP_INFO(this->get_logger(), "Service: /morse_encode");
        RCLCPP_INFO(this->get_logger(), "Publisher: /morse_code");
    }

private:
    std::string text_to_morse(const std::string &text) const
    {
        std::ostringstream result;

        bool first_symbol = true;
        bool previous_was_space = false;

        for (char raw_char : text)
        {
            if (std::isspace(static_cast<unsigned char>(raw_char)))
            {
                if (!first_symbol && !previous_was_space)
                {
                    result << " / ";
                    previous_was_space = true;
                }
                continue;
            }

            char upper_char = static_cast<char>(
                std::toupper(static_cast<unsigned char>(raw_char)));

            auto found = morse_code_.find(upper_char);

            if (found == morse_code_.end())
            {
                throw std::runtime_error(
                    std::string("Unsupported character: ") + raw_char);
            }

            if (!first_symbol && !previous_was_space)
            {
                result << " ";
            }

            result << found->second;

            first_symbol = false;
            previous_was_space = false;
        }
        return result.str();
    }

    void encode_callback(
        const std::shared_ptr<morse_interfaces::srv::MorseEncode::Request> request,
        std::shared_ptr<morse_interfaces::srv::MorseEncode::Response> response)
    {
        try
        {
            const std::string morse = text_to_morse(request->text);

            response->success = true;
            response->morse = morse;
            response->message = "Encoded successfully.";

            std_msgs::msg::String msg;
            msg.data = morse;
            morse_publisher_->publish(msg);

            RCLCPP_INFO(this->get_logger(), "Text: %s", request->text.c_str());
            RCLCPP_INFO(this->get_logger(), "Morse: %s", morse.c_str());
            RCLCPP_INFO(this->get_logger(), "Published to /morse_code");
        }
        catch (const std::exception &error)
        {
            response->success = false;
            response->morse = "";
            response->message = error.what();

            RCLCPP_WARN(this->get_logger(), "%s", error.what());
        }
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MorseEncoderServiceNode>());
    rclcpp::shutdown();

    return 0;
}
