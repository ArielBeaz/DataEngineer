from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os

# Importar funciones de tu script
from youtube_etl import main

# Definir argumentos y propiedades del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Crear el DAG
with DAG(
    'youtube_etl_dag',
    default_args=default_args,
    description='DAG para extraer y cargar datos de YouTube a Redshift',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Definir la tarea que ejecuta la función main
    run_etl = PythonOperator(
        task_id='run_youtube_etl',
        python_callable=main,
    )

    run_etl