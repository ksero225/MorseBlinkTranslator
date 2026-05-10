# MorseBlinkTranslator

A ROS 2 project for translating text into Morse code, blinking it on an OLED display, and decoding the light signal back into text using a Raspberry Pi camera.

## Overview

**MorseBlinkTranslator** is a Raspberry Pi + ROS 2 project focused on encoding and decoding Morse code using light signals.

The system first converts normal ASCII text into Morse code. Then, the encoded message is displayed as a blinking signal on an SSD1306 OLED display. In the next stage, a Raspberry Pi camera observes the blinking display and attempts to decode the signal back into readable text.

## Features

- Convert ASCII text into Morse code
- Publish Morse code through ROS 2 communication
- Blink Morse code on an OLED display
- Read the blinking signal using a Raspberry Pi camera
- Decode light pulses into Morse code
- Translate decoded Morse code back into normal text

## Hardware

The project is designed to run on a Raspberry Pi setup with an external OLED display and camera module.

Used hardware:

- Raspberry Pi 5
- Raspberry Pi Camera HD v3 12MPx
- SSD1306 OLED display, 128x64, I2C
- Jumper wires
- Breadboard, optional
- microSD card with Linux system installed

## Technologies

- ROS 2 Jazzy
- C++
- Python
- CMake
- Raspberry Pi
- I2C
- SSD1306 OLED display
- Raspberry Pi Camera HD v3
- libcamera
- OpenCV

## Project Architecture

The project is divided into several ROS 2 nodes. Each node is responsible for one part of the Morse translation pipeline.

```text
ASCII text
    |
    v
Morse Encoder Node
    |
    v
Morse Code Topic
    |
    v
OLED Blink Node
    |
    v
Blinking OLED Display
    |
    v
Raspberry Pi Camera
    |
    v
Camera Decoder Node
    |
    v
Decoded Text
```

## Installation

```bash
# Clone the repository
git clone https://github.com/ksero225/MorseBlinkTranslator.git
cd MorseBlinkTranslator

# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Install dependencies
rosdep install -i --from-path src --rosdistro jazzy -y

# Build the workspace
colcon build --symlink-install

# Source the local workspace
source install/setup.bash
```
