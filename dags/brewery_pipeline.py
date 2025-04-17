# dags/brewery_pipeline.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import json
import os

default_args = {
    "owner": "Bees",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Extrair os dados
def extract():
    url = "https://api.openbrewerydb.org/v1/breweries"
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Garante que uma exceção seja levantada se houver erro
    data = response.json()

    os.makedirs("data/bronze", exist_ok=True)
    with open("data/bronze/breweries.json", "w") as f:
        json.dump(data, f)

# Transformar os dados e salvar particionado por estado
def transform():
    os.makedirs("data/silver", exist_ok=True)
    df = pd.read_json("data/bronze/breweries.json")
    df.to_parquet("data/silver/breweries.parquet", partition_cols=["state"], index=False)

# Agregar os dados por tipo e estado
def aggregate():
    os.makedirs("data/gold", exist_ok=True)
    df = pd.read_parquet("data/silver/breweries.parquet")
    agg = df.groupby(["state", "brewery_type"]).size().reset_index(name="count")
    agg.to_parquet("data/gold/brewery_summary.parquet", index=False)

# Definição da DAG
with DAG(
    dag_id="brewery_data_pipeline",
    default_args=default_args,
    description="Pipeline ETL para dados de cervejarias usando Airflow",
    schedule_interval="@daily",  # Executa 1x por dia
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=["brewery", "etl", "data_pipeline"]
) as dag:

    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract
    )

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform
    )

    task_aggregate = PythonOperator(
        task_id="aggregate_data",
        python_callable=aggregate
    )

    task_extract >> task_transform >> task_aggregate
