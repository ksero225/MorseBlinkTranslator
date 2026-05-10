import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image


class OledBlinkNode(Node):
    def __init__(self):
        super().__init__('oled_blink_node')

        self.subscription = self.create_subscription(
            String,
            'morse_code',
            self.morse_callback,
            10
        )

        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, width=128, height=64)

        self.dot_time = 0.2
        self.dash_time = self.dot_time * 3
        self.symbol_gap = self.dot_time
        self.letter_gap = self.dot_time * 3
        self.word_gap = self.dot_time * 7

        self.white = Image.new("1", (128, 64), 1)

        self.device.display(self.white)
        self.device.hide()

        self.get_logger().info(
            "OLED blink node started. Waiting for Morse code on topic: morse_code"
        )

    def morse_callback(self, msg):
        morse_text = msg.data.strip()

        self.get_logger().info(f"Received Morse: {morse_text}")

        for char in morse_text:
            if char == '.':
                self.blink(self.dot_time)
                time.sleep(self.symbol_gap)

            elif char == '-':
                self.blink(self.dash_time)
                time.sleep(self.symbol_gap)

            elif char == ' ':
                time.sleep(self.letter_gap)

            elif char == '/':
                time.sleep(self.word_gap)

        self.clear_screen()

    def blink(self, duration):
        self.screen_on()
        time.sleep(duration)
        self.screen_off()

    def screen_on(self):
        self.device.show()

    def screen_off(self):
        self.device.hide()

    def clear_screen(self):
        self.device.hide()


def main(args=None):
    rclpy.init(args=args)

    node = OledBlinkNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.clear_screen()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()