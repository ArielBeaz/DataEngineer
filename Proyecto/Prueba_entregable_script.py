import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from pandas import json_normalize

load_dotenv()

#conectarse a la API de YT

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
API_URL = 'https://www.googleapis.com/youtube/v3/videos'

params = {
        'part': 'snippet,statistics',
        'chart': 'mostPopular',
        'regionCode': 'CL',
        'maxResults': 10, 
        'key': YOUTUBE_API_KEY}

response = requests.get(API_URL, params=params)
data = response.json()

#Pasar a dataframe el contenido de la API y hacer un ETL para tener un DataFrame a cargar en Redshift

df = json_normalize(data['items'])
new_index = ['titulo', 'canal_id','reproducciones','cantidad_de_likes','cantidad_comentarios','lenguaje']
dfredshift = df[['snippet.title','snippet.channelId','statistics.viewCount','statistics.likeCount','statistics.commentCount','snippet.defaultLanguage']]
dfredshift.columns=new_index

time_request = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dfredshift['time_request'] = str(time_request)

dtypes= dfredshift.dtypes
cols= list(dtypes.index )
values = [tuple(x) for x in dfredshift.to_numpy()]


db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host_amazon = os.getenv('db_host_amazon')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')

try:
    conn = psycopg2.connect(
    host=db_host_amazon,
    dbname=db_name,
    user=db_user,
    password=db_password,
    port=db_port
    )
    print("Connected to Redshift successfully!")
    
except Exception as e:
    print("Unable to connect to Redshift.")
    print(e)


query_create_table = f"""
    CREATE TABLE IF NOT EXISTS ariel_beaz_coderhouse.tendencias_youtube (
    titulo VARCHAR(500),
    canal_id VARCHAR(200),
    reproducciones INT,
    cantidad_de_likes INT,
    cantidad_comentarios INT,
    lenguaje VARCHAR(200),
    time_request VARCHAR(200)
);
"""

cur = conn.cursor()
cur.execute(query_create_table)

insert_sql = f"INSERT INTO ariel_beaz_coderhouse.tendencias_youtube({', '.join(cols)}) VALUES %s"

cur.execute("BEGIN")
execute_values(cur, insert_sql, values)
cur.execute("COMMIT")
