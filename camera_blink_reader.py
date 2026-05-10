import time

import cv2
from picamera2 import Picamera2


MORSE_TO_TEXT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",

    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
}


class BlinkReader:
    def __init__(self):
        self.dot_time = 0.2
        self.dash_time = self.dot_time * 3

        self.symbol_gap = self.dot_time
        self.letter_gap = self.dot_time * 3
        self.word_gap = self.dot_time * 7

        # Jak nie wykrywa dobrze, zmienisz ten próg.
        self.brightness_threshold = 80

        self.last_state = None
        self.last_change_time = time.time()

        self.current_morse = ""
        self.decoded_text = ""

    def process_state(self, current_state, brightness):
        now = time.time()

        if self.last_state is None:
            self.last_state = current_state
            self.last_change_time = now
            print(
                f"Initial brightness: {brightness:.2f}, "
                f"state: {'ON' if current_state else 'OFF'}"
            )
            return

        if current_state == self.last_state:
            return

        duration = now - self.last_change_time

        print(
            f"State changed: "
            f"{'ON' if self.last_state else 'OFF'} -> "
            f"{'ON' if current_state else 'OFF'}, "
            f"duration: {duration:.3f}s, "
            f"brightness: {brightness:.2f}"
        )

        if self.last_state:
            self.handle_light_duration(duration)
        else:
            self.handle_dark_duration(duration)

        self.last_state = current_state
        self.last_change_time = now

    def handle_light_duration(self, duration):
        border = (self.dot_time + self.dash_time) / 2

        if duration < border:
            self.current_morse += "."
            print(f"DOT detected: {self.current_morse}")
        else:
            self.current_morse += "-"
            print(f"DASH detected: {self.current_morse}")

    def handle_dark_duration(self, duration):
        symbol_letter_border = (self.symbol_gap + self.letter_gap) / 2
        letter_word_border = (self.letter_gap + self.word_gap) / 2

        # Krótka przerwa między kropką/kreską.
        if duration < symbol_letter_border:
            return

        # Średnia przerwa — koniec litery.
        if duration < letter_word_border:
            self.finish_letter()
            return

        # Długa przerwa — koniec słowa.
        self.finish_letter()

        if self.decoded_text and not self.decoded_text.endswith(" "):
            self.decoded_text += " "
            print("WORD GAP")
            print(f"TEXT: {self.decoded_text}")

    def finish_letter(self):
        if not self.current_morse:
            return

        letter = MORSE_TO_TEXT.get(self.current_morse, "?")
        self.decoded_text += letter

        print(f"LETTER: {self.current_morse} -> {letter}")
        print(f"TEXT: {self.decoded_text}")

        self.current_morse = ""


def main():
    reader = BlinkReader()

    picam2 = Picamera2()

    picam2.configure(
        picam2.create_preview_configuration(
            main={
                "format": "RGB888",
                "size": (640, 480),
            }
        )
    )

    picam2.start()
    time.sleep(1.0)

    print("Camera blink reader started.")
    print("Put OLED in the center of the camera frame.")
    print("Press Ctrl+C to stop.")
    print()

    try:
        while True:
            frame = picam2.capture_array()

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            height, width = gray.shape

            # Środek kadru.
            x1 = int(width * 0.35)
            x2 = int(width * 0.65)
            y1 = int(height * 0.35)
            y2 = int(height * 0.65)

            roi = gray[y1:y2, x1:x2]
            avg_brightness = roi.mean()

            current_state = avg_brightness > reader.brightness_threshold

            reader.process_state(current_state, avg_brightness)

            time.sleep(0.02)

    except KeyboardInterrupt:
        print()
        print("Stopped.")
        print(f"Final text: {reader.decoded_text}")

    finally:
        picam2.stop()


if __name__ == "__main__":
    main()
