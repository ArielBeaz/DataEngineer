import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from pandas import json_normalize
import isodate

load_dotenv()

def get_youtube_data(api_key, max_results=10, region_code='CL'):
    API_URL = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,statistics,contentDetails',
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

def convert_to_minutes(duration):
    if pd.isna(duration):
        return None
    duration_obj = isodate.parse_duration(duration)
    return duration_obj.total_seconds() / 60

def transform_data(data):
    df = json_normalize(data['items'])
    dfredshift = df[['id', 'snippet.title', 'snippet.channelId', 'statistics.viewCount',
                     'statistics.likeCount', 'statistics.commentCount', 'contentDetails.duration',
                     'snippet.defaultLanguage']]
    new_index = ['id', 'titulo', 'canal_id', 'reproducciones', 'cantidad_de_likes', 
                 'cantidad_comentarios', 'duración', 'lenguaje']
    dfredshift.columns = new_index
    
    # Convertir la duración a minutos y agregar time_request
    dfredshift['duración_minutos'] = dfredshift['duración'].apply(convert_to_minutes)
    dfredshift = dfredshift.drop(columns=['duración'])
    time_request = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dfredshift['time_request'] = str(time_request)
    
    return dfredshift

def connect_to_redshift(db_user, db_password, db_host, db_port, db_name):
    try:
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("Connected to Redshift successfully!")
        return conn
    except Exception as e:
        print("Unable to connect to Redshift.")
        print(e)
        return None

def create_table(conn, table_name):
    query_create_table = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        id VARCHAR(50),
        titulo VARCHAR(500),
        canal_id VARCHAR(200),
        reproducciones INT,
        cantidad_de_likes INT,
        cantidad_comentarios INT,
        lenguaje VARCHAR(200),
        duración_minutos FLOAT,
        time_request VARCHAR(200),
        PRIMARY KEY (id, time_request)
    );
    """
    cur = conn.cursor()
    cur.execute(query_create_table)
    cur.close()

def consult_table(conn, table_name):
    query_consult_table = f"""
       SELECT *
       FROM {table_name};
    """
    cur = conn.cursor()
    cur.execute(query_consult_table)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    cur.close()
    return df

def insert_data(conn, table_name, df):
    dtypes = df.dtypes
    cols = list(dtypes.index)
    values = [tuple(x) for x in df.to_numpy()]
    insert_sql = f"""
        INSERT INTO {table_name} ({', '.join(cols)}) 
        VALUES %s
    """
    cur = conn.cursor()
    cur.execute("BEGIN")
    execute_values(cur, insert_sql, values)
    cur.execute("COMMIT")
    cur.close()

def main():
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    db_user = os.getenv('db_user')
    db_password = os.getenv('db_password')
    db_host_amazon = os.getenv('db_host_amazon')
    db_port = os.getenv('db_port')
    db_name = os.getenv('db_name')
    
    data = get_youtube_data(YOUTUBE_API_KEY)
    dfredshift = transform_data(data)
    
    conn = connect_to_redshift(db_user, db_password, db_host_amazon, db_port, db_name)
    if conn:
        table_name = "ariel_beaz_coderhouse.tendencias_youtube"
        create_table(conn, table_name)
        insert_data(conn, table_name, dfredshift)
        df_result = consult_table(conn, table_name)
        print(df_result)
        conn.close()

if __name__ == "__main__":
    main()