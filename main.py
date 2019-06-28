# coding=utf-8

import logging
import multiprocessing
import time

import RPi.GPIO as GPIO
import configparser

from lcd_manager import LcdManager
from context_manager import MainScreenContext, download_weather_data

config = configparser.ConfigParser()
config.read('config.ini')

logging.getLogger().setLevel(logging.INFO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.info("GPIO successfully initiated")


def lcd_main_loop(weather_data, lcd_manager):
    def_screen = MainScreenContext(config)
    while True:
        def_screen.set_weather_data(weather_data)
        lines = def_screen.get_lines()
        lcd_manager.set_lines(*lines)
        lcd_manager.update()

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)


def update_weather_data(weather_data):
    while True:
        desc, temp = download_weather_data(config)
        weather_data[0] = desc
        weather_data[1] = temp

        time.sleep(60 * int(config["weather"]["weather_update"]))


if __name__ == '__main__':
    process_manager = multiprocessing.Manager()
    lcd_manager = LcdManager(config)

    manager = multiprocessing.Manager()
    weather_data = manager.list(["Weather service unavailable", "N/A"])

    lcd_screen_update_process = multiprocessing.Process(target=lcd_main_loop, args=(weather_data, lcd_manager))
    update_weather_process = multiprocessing.Process(target=update_weather_data, args=(weather_data,))


    try:
        lcd_screen_update_process.start()
        update_weather_process.start()

        lcd_screen_update_process.join()
        update_weather_process.join()

    except KeyboardInterrupt:
        pass

    finally:
        lcd_screen_update_process.terminate()
        update_weather_process.terminate()
        lcd_manager.close()
        GPIO.cleanup()
        logging.info("good bye")
