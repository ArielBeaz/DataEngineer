import requests
import json

url = 'https://data.messari.io/api/v1/assets/bitcoin/metrics'
response = requests.get(url)
response_json = response.json()

fecha = response_json['status']['timestamp']
volumen = response_json['data']['market_data']['volume_last_24_hours']
open = response_json['data']['market_data']['ohlcv_last_1_hour']['open']
high = response_json['data']['market_data']['ohlcv_last_1_hour']['high']
low = response_json['data']['market_data']['ohlcv_last_1_hour']['low']
close = response_json['data']['market_data']['ohlcv_last_1_hour']['close']

bitcoin = {}
bitcoin[fecha] = {'fecha' :fecha , 'volumen' : volumen ,'open' : open , 'high': high , 'low': low , 'close': close}

print(bitcoin)