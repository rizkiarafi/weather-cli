from dotenv import load_dotenv
import requests
import os
import socket

def get_ip6():
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    user_ip = addresses[2][4][0]

    return user_ip

iplocate_api_key = os.getenv("IPLOCATE_API_KEY")