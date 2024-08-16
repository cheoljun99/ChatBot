import requests
from config import conf

URLSCAN_API_KEY = conf['urlscan_api_key']

def urlscan_query(url):
    headers = {
        "API-Key": URLSCAN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"url": url, "visibility": "public"}
    response = requests.post("https://urlscan.io/api/v1/scan/", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve data: {response.status_code}"}
