from airflow import DAG
from asyncio import tasks
from textwrap import dedent
import datetime
import pendulum
import json
from airflow.operators.python import PythonOperator
import os


with DAG(
    dag_id="sensor_training" , 
    default_args={'retries' : 2 },
    schedule="@weekly" , 
    description="Sensor Fault Detection",
    start_date= pendulum.datetime(2023 , 5 , 5 , tz='CET'),
    catchup=False , 
    tags=["example"],
    ) as dag:




    def training(**kwargs):
        from sensor.pipeline.training_pipeline import start_training_pipline
        start_training_pipline()


    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")

        training_pipeline  = PythonOperator(
                task_id="train_pipeline",
                python_callable=training

        )

        sync_data_to_s3 = PythonOperator(
                task_id="sync_data_to_s3",
                python_callable=sync_artifact_to_s3_bucket

    )

        training_pipeline >> sync_data_to_s3

    