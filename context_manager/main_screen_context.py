import time


class MainScreenContext:
    def __init__(self, config):
        self.temp = ""
        self.wind = ""

    def get_lines(self):
        return self.get_time_line(), self.get_weather_line()

    def get_time_line(self):
        time_string = time.strftime("%d/%m %H:%M", time.localtime())+ " " + self.temp + '\x02'
        return time_string

    def get_weather_line(self):
        return "Wiatr: "+self.wind + "km/h"

    def set_weather_data(self, weather_data):
        self.wind = weather_data[0]
        self.temp = weather_data[1]
