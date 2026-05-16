from dotenv import load_dotenv
import requests
import os
import socket
import json

def load_json(data_file):
    try:
        with open(data_file, "r") as read:
            ip_cache = json.load(read)
            return ip_cache
    except FileNotFoundError:
        return None

def write_json(content, data_file):
    with open(data_file, "w") as write:
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
    load_dotenv()
    iplocate_api_key = os.getenv("IPLOCATE_API_KEY")

    ip6 = get_ip6()

    geo_data = None
    geo_cache = load_json("ip-geo-cache.json")

    BASE_URL = "https://iplocate.io/api/lookup/"
    url = f"{BASE_URL}{ip6}?apikey={iplocate_api_key}"

    if geo_cache:
        if ip6 == geo_cache["user_ip"]:
            print("Using cache if exists when the IP is the same with previous IP")
            geo_data = geo_cache
            return geo_data
    
    response = requests.get(url)

    if response.status_code == 200:
        geo_data = response.json()
        geo_data["user_ip"] = ip6
        write_json(geo_data, "ip-geo-cache.json")
        print("Requesting success!")
    else:
        if geo_cache:
            geo_data = geo_cache
            print("Using cache if exists when the API throws an error")
            print(f"ERROR: {response.status_code}")

    return geo_data

print(fetch_ip_geo_api())