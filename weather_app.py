from weather_data import fetch_weather_api
from datetime import datetime
import pandas as pd

weather_stamps = 40
per_day_index = [round(weather_stamps / 5) * i for i in range(5)]

weather_data = fetch_weather_api()

if weather_data:
    for day, weather_stamp in enumerate(per_day_index):
        dt = weather_data["list"][weather_stamp]["dt"]
        formatted_dt = datetime.fromtimestamp(dt)
        weather = weather_data["list"][weather_stamp]["weather"][0]["description"]
        
        print(formatted_dt.strftime("%A"))
        print(formatted_dt)
        print(weather, end="\n\n")
else:
    print("None!")