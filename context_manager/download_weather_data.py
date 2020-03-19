import logging

import requests


def download_weather_data(config):
    config = config["weather"]
    api_key = config["openweathermap_key"]
    location = config["location"]
    lang = config["lang"]
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang={}" \
        .format(location, api_key, lang)

    try:
        r = requests.get(url)
        j = r.json()

        wind = str(j['wind']['speed'])
        temp = str(int(j['main']['temp']))
    except requests.exceptions.RequestException:
        logging.warning("Can't reach weather service")
        wind = ""
        temp = ""
    finally:
        return wind, temp
