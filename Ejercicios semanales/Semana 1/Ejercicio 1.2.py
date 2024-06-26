import requests
import json

url = 'tps://data.messari.io/api/v1/assets/bitcoin/metrics'
response = requests.get(url)

response_json = response.json()


print(response_json)