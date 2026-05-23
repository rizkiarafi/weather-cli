from datetime import datetime
import pandas as pd
from weather_data import fetch_weather_api


def main() -> None:
    """Fetches weather forecast data and displays a 5-day daily summary."""
    weather_stamps = 40
    # Downsample to 5 indices, representing approximately one reading per day (every 24 hours)
    per_day_index = [round(weather_stamps / 5) * i for i in range(5)]

    weather_data = fetch_weather_api()

    if not weather_data:
        print("No weather data could be retrieved.")
        return

    five_days_weather = []
    for weather_stamp in per_day_index:
        weather = weather_data["list"][weather_stamp]
        
        # Extract forecast details
        timestamp = weather["dt"]
        weather_desc = weather["weather"][0]["description"]
        temperature = weather["main"]["temp_max"]
        humidity = weather["main"]["humidity"]
        formatted_date = datetime.fromtimestamp(timestamp)
        
        weather_dict = {
            "date": formatted_date,
            "weather": weather_desc,
            "celsius_temperature": temperature,
            "humidity": humidity
        }
        five_days_weather.append(weather_dict)

    # Output formatted forecast as a DataFrame table
    df = pd.DataFrame(five_days_weather)
    print(df)


if __name__ == "__main__":
    main()