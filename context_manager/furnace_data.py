import logging

import requests
import xml.etree.ElementTree as ET


def download_furnace_data(config):
    config = config["furnace"]
    login = config["login"]
    password = config["password"]
    ip_address = config["ip_address"]
    url = "http://{}:{}@{}/getregister.cgi?".format(login, password, ip_address)+"{}"
    fuel_level = ""
    furnace_temp = ""

    try:
        fuel_level = __get_data(url, "fuel_level")
        furnace_temp = __get_data(url, "tkot_value")
        furnace_temp = furnace_temp[:4]
    except requests.exceptions.RequestException:
        logging.warning("Can't reach furnace")
        fuel_level = ""
        furnace_temp = ""
    finally:
        return fuel_level, furnace_temp


def __get_data(url,command):
    url = url.format(command)
    data = requests.get(url)
    data = ET.fromstring(data.text)
    return data[0][0].get('v')
