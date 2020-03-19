# coding=utf-8

import logging
import multiprocessing
import time

import RPi.GPIO as GPIO
import configparser

from context_manager.check_light_level import check_light_level
from context_manager.furnace_data import download_furnace_data
from lcd_manager import LcdManager
from context_manager import MainScreenContext, download_weather_data

config = configparser.ConfigParser()
config.read('config.ini')

logging.getLogger().setLevel(logging.INFO)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.info("GPIO successfully initiated")


def lcd_main_loop(data, lcd_manager):
    def_screen = MainScreenContext(config)
    max_light = int(config["lcd_manager"]["max_light"])
    while True:
        def_screen.set_data(data)
        lines = def_screen.get_lines()
        lcd_manager.set_lines(*lines)
        lcd_manager.update()

        light_level = check_light_level(config)
        if light_level == max_light: lcd_manager.turn_off_backlight()
        else: lcd_manager.turn_on_backlight()

        tim = time.time()
        tim = abs(tim % 1 - 1)
        time.sleep(tim)


def update_data(data):
    slow_tick = int(config["furnace"]["furnace_update"])
    weather_tick_limit = int(int(config["weather"]["weather_update"]) / slow_tick)
    weather_tick = weather_tick_limit
    while True:
        if(weather_tick < weather_tick_limit): weather_tick+=1
        else:
            desc, temp = download_weather_data(config)
            weather_tick = 0

        fuel_level, furnace_temp = download_furnace_data(config)

        data[0] = temp
        data[1] = furnace_temp
        data[2] = fuel_level

        time.sleep(60 * slow_tick)


if __name__ == '__main__':
    process_manager = multiprocessing.Manager()
    lcd_manager = LcdManager(config)

    manager = multiprocessing.Manager()
    data = manager.list(["", "", ""])

    lcd_screen_update_process = multiprocessing.Process(target=lcd_main_loop, args=(data, lcd_manager))
    update_weather_process = multiprocessing.Process(target=update_data, args=(data,))

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
