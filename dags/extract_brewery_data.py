from __future__ import annotations

import pendulum
from datetime import timedelta
from airflow.sdk import ObjectStoragePath, dag, task
from pyspark.sql import SparkSession


api_url = "https://api.openbrewerydb.org/v1/breweries"

base = ObjectStoragePath("s3://airflow-brewery-list/", conn_id="AWS_CONNECTION")


def on_failure_callback(context):
    """
    Callback function to handle task failures.
    This can be used to send notifications or log errors.
    """
    # Implement your failure handling logic here
    print(f"Task failed: {context['task_instance'].task_id} at {context['ts']}")


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    on_failure_callback=on_failure_callback,
)
def run_pipeline_brewery():
    """
    Run a pipeline to extract brewery data from an API, save it in S3, and process it using PySpark.
    """


    @task(retries=3, retry_delay=timedelta(seconds=5))
    def extract_data(**kwargs):
        """
        #### Get Air Quality Data
        This task gets air quality data from the Finnish Meteorological Institute's
        open data API. The data is saved as parquet.
        """
        
        from extract_data_api import ExtractDataAPI
        
        base.mkdir(exist_ok=True)
        path = base / "bronze" / f"brewery_list.json"
        extract = ExtractDataAPI(api_url)
        response = extract.fetch_data()
        json_bytes = extract.convert_to_bytes(response)
        extract.write_file(path, json_bytes)
    
    
    @task.pyspark(config_kwargs={"spark.jars.packages": "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.787"})
    def save_silver_layer(spark: SparkSession):
        """
        Save the extracted data to the silver layer in S3.
        """
            
        from save_silver_layer import SaveSilverLayer
        
        process_json_file = SaveSilverLayer(spark)
        process_json_file.process()
    
    
    @task.pyspark(config_kwargs={"spark.jars.packages": "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.787"})
    def save_gold_layer(spark: SparkSession):
        """
        Save the processed data to the gold layer in S3.
        """
            
        from save_gold_layer import SaveGoldLayer
        
        process_json_file = SaveGoldLayer(spark)
        process_json_file.process()


    # [START main_flow]
    extract_data() >> save_silver_layer() >> save_gold_layer()
    # [END main_flow]


run_pipeline_brewery()
