import requests
import os
import json

url = "https://api.giphy.com/v1/gifs/trending"
params = {'api_key': os.environ.get("GIPHY_API_KEY"), 'limit': 10}
response = requests.get(url, params)
if response.status_code == 200:
    json_response = response.json()
    for gif in json_response['data']:
        print("---------")
        pretty_json = json.dumps(gif, indent=4)
        print(pretty_json)
