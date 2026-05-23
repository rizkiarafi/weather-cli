from dotenv import load_dotenv
from pathlib import Path
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
import requests
import os
import socket
import json
import time
import inspect

load_dotenv()

OPENWEATHERMAP_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
IPLOCATE_BASE_URL = "https://iplocate.io/api/lookup/"

CACHE_FILEPATH = Path("./cache-data")

CONNECT_TIMEOUT_DURATION = 3.05
READ_TIMEOUT_DURATION = 21

weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
iplocate_api_key = os.getenv("IPLOCATE_API_KEY")

def load_json(data_file: str):
    json_filepath = CACHE_FILEPATH / data_file
    if json_filepath.exists():
        with open(json_filepath, "r") as read:
            ip_cache = json.load(read)
            return ip_cache
    else:
        return None

def write_json(content, data_file):
    CACHE_FILEPATH.mkdir(parents=True, exist_ok=True)
    json_filepath = CACHE_FILEPATH / data_file
    with open(json_filepath, "w") as write:
        json.dump(content, write, indent=2)

def get_ip6():
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    try:
        user_ip = {"ip": addresses[1][4][0]}
        ip6 = user_ip["ip"]
        write_json(user_ip, "ip-cache.json")
    except IndexError:
        ip_cache = load_json("ip-cache.json")
        ip6 = ip_cache["ip"] if ip_cache != None else None

    return ip6

def fetch_ip_geo_api():
    ip6 = get_ip6()
    geo_data = None
    geo_cache = load_json("ip-geo-cache.json")

    url = f"{IPLOCATE_BASE_URL}{ip6}?apikey={iplocate_api_key}"
    function_name = inspect.currentframe().f_code.co_name

    if geo_cache:
        if ip6 == geo_cache["user_ip"]:
            geo_data = geo_cache
            print(f"{function_name}: Used cache if exists when the IP is the same with previous IP")
            return geo_data
    
    try:
        response = requests.get(url, timeout=(CONNECT_TIMEOUT_DURATION, READ_TIMEOUT_DURATION))
    except ConnectionError:
        print(f"ConnectionError in {function_name}: You have no internet connection!")
    except ConnectTimeout:
        print(f"ConnectTimeout in {function_name}: Your internet is too slow to send request")
    except ReadTimeout:
        print(f'ConnectTimeout in {function_name}: "{url}" takes too long to send back response')
    else:
        if response.status_code == 200:
            geo_data = response.json()
            geo_data["user_ip"] = ip6
            write_json(geo_data, "ip-geo-cache.json")
            print(f"{function_name}: Requesting success!")
        else:
            if geo_cache:
                geo_data = geo_cache
                print(f"{function_name}: Used cache if exists when the API throws an error")
                print(f"ERROR: {response.status_code}")

    return geo_data

def fetch_weather_api():
    weather_data = None
    weather_cache = load_json("weather-cache.json")
    function_name = inspect.currentframe().f_code.co_name
    update_duration = 60
    geo_data = fetch_ip_geo_api()
    if weather_cache:
        weather_data = weather_cache["data"]
        weather_cache_age = round(time.time()) - weather_cache["fetch_dt"]
        if weather_cache_age < update_duration and weather_cache["ip"] == geo_data["ip"]:
            print(f"{function_name}: Used cache if exists and its age is less than {update_duration} seconds")
            return weather_data
        else:
            print(f"{function_name}: Updating the cache because the cache is expired or using different IP Address")
    
    if geo_data:
        lat = geo_data["latitude"]
        lon = geo_data["longitude"]

        url = f"{OPENWEATHERMAP_BASE_URL}?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
        try:
            response = requests.get(url)
        except ConnectionError:
            print(f"ConnectionError in {function_name}: You have no internet connection!")
        except ConnectTimeout:
            print(f"ConnectTimeout in {function_name}: Your internet is too slow to send request")
        except ReadTimeout:
            print(f'ConnectTimeout in {function_name}: "{url}" takes too long to send back response')
        else:
            if response.status_code == 200:
                weather_data = {
                    "fetch_dt": round(time.time()),
                    "ip": geo_data["ip"],
                    "data": response.json()
                }
                print(f"{function_name}: Requesting success!")
                write_json(weather_data, "weather-cache.json")
                weather_data = weather_data["data"]
            else:
                print(f"ERROR: {response.status_code}")
                if weather_cache:
                    weather_data = weather_cache

    return weather_data