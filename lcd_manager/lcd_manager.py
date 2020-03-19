# coding=utf-8
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

from .register_char import register_char
from .text_line import TextLine


class LcdManager:
    def __init__(self, config):
        config = config['lcd_manager']
        self.dimmer_pin = int(config['dimmer_pin'])
        GPIO.setup(self.dimmer_pin, GPIO.OUT)
        self.turn_on_backlight()

        self.lcd_width = int(config['width'])

        self.lcd = CharLCD(
            pin_rs=int(config['rs']),
            pin_e=int(config['e']),
            pins_data=[int(y) for y in config['data_pins'].split(",")],
            auto_linebreaks=True,
            numbering_mode=GPIO.BCM,
            cols=self.lcd_width
        )

        for foo, bar in zip(range(len(register_char)), register_char):
            self.lcd.create_char(foo, bar)

        self.lines = [
            TextLine('', self.lcd_width),
            TextLine('', self.lcd_width)
        ]

    def turn_on_backlight(self):
        GPIO.output(self.dimmer_pin, GPIO.HIGH)

    def turn_off_backlight(self):
        GPIO.output(self.dimmer_pin, GPIO.LOW)

    def close(self):
        self.turn_off_backlight()
        self.lcd.close(clear=True)

    def set_lines(self, line, line2):
        self.lines[0].set_text(line)
        self.lines[1].set_text(line2)

    def update(self):
        i = 0
        for line in self.lines:
            self.lcd.cursor_pos = (i, 0)
            self.lcd.write_string(str(line).ljust(self.lcd_width))
            i += 1
