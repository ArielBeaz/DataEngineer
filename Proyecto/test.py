import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from pandas import json_normalize

load_dotenv()

def get_youtube_data(api_key, max_results=10, region_code='CL'):
    API_URL = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,statistics',
        'chart': 'mostPopular',
        'regionCode': region_code,
        'maxResults': max_results,
        'key': api_key
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from YouTube API: {response.status_code}")
        return None
    
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
data = get_youtube_data(YOUTUBE_API_KEY)
