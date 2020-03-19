import time


class MainScreenContext:
    def __init__(self, config):
        self.temp = ""
        self.furnace_temp = ""
        self.fuel_level = ""

    def get_lines(self):
        return self.get_time_line(), self.get_second_line()

    def get_time_line(self):
        if self.temp == "": temp = "N/A"
        else: temp = self.temp
        time_string = time.strftime("%d/%m %H:%M", time.localtime())+ " " + temp + '\x02'
        return time_string

    def get_second_line(self):
        if self.furnace_temp == "":
            furnace_temp = "N/A"
            fuel_level = "N/A"
        else:
            furnace_temp = self.furnace_temp
            fuel_level = self.fuel_level
        return "K: "+furnace_temp +  '\x02'+ " P: "+fuel_level+"%"

    def set_data(self, data):
        self.temp = data[0]
        self.furnace_temp = data[1]
        self.fuel_level = data[2]
