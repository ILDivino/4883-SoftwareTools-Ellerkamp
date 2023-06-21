import GUI_helper
import Scrapper_helper
import re

url = GUI_helper.buildWeatherURL()
#print(url)
Scrapper_helper.scrape_airport_weather_day(url)
