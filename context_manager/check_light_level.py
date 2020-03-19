import RPi.GPIO as GPIO
import time


def check_light_level(config):
    photoresistor_pin = 14
    max_light = int(config["lcd_manager"]["max_light"])
    reading = 0
    GPIO.setup(photoresistor_pin, GPIO.OUT)
    GPIO.output(photoresistor_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(photoresistor_pin, GPIO.IN)
    while (GPIO.input(photoresistor_pin) == GPIO.LOW):
        time.sleep(0.1)
        reading += 1
        if reading==max_light: break
    return reading
