# Usar la imagen oficial de Apache Airflow como base
FROM apache/airflow:2.6.3-python3.9

# Establecer variables de entorno para la configuración de Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Instalar las dependencias necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el DAG a la carpeta de dags
COPY dags/ /opt/airflow/dags/