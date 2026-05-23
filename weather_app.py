from weather_data import fetch_weather_api
from datetime import datetime
import pandas as pd

weather_stamps = 40
per_day_index = [round(weather_stamps / 5) * i for i in range(5)]

weather_data = fetch_weather_api()

if weather_data:
    five_days_weather = []
    for weather_stamp in (per_day_index):
        weather = weather_data["list"][weather_stamp]
        dt = weather["dt"]
        weather_desc = weather["weather"][0]["description"]
        temprature = weather["main"]["temp_max"]
        humidity = weather["main"]["humidity"]
        formatted_dt = datetime.fromtimestamp(dt)
        
        weather_dict = {
            "date": formatted_dt,
            "weather": weather_desc,
            "celc_temprature": temprature,
            "humidity": humidity
        }

        five_days_weather.append(weather_dict)

    print(pd.DataFrame(five_days_weather))
else:
    print("None!")