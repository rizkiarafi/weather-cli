from dotenv import load_dotenv
import requests
import os
import socket
import json

def get_ip6():
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    user_ip = addresses[2][4][0]

    return user_ip

def fetch_ip_geo_api():
    load_dotenv()
    iplocate_api_key = os.getenv("IPLOCATE_API_KEY")
    ip6 = get_ip6()

    BASE_URL = "https://iplocate.io/api/lookup/"
    url = f"{BASE_URL}{ip6}?apikey={iplocate_api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("success!")
        return data
    else:
        print(f"ERROR: {response.status_code}")
        return None