"""This module defines a class to process a JSON file from an S3 bucket using PySpark.
"""
import os
from pyspark.sql import SparkSession


class SaveSilverLayer:
    
    BUCKET_NAME = "airflow-brewery-list"
    LAYER_READ = "bronze"
    LAYER_TYPE = "silver"
    

    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default_value')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default_value')
        
        self.log4jLogger = spark._jvm.org.apache.log4j.LogManager.getLogger(__name__)


    def process(self, prefix: str = "s3a://"):

        self.spark.conf.set('spark.hadoop.fs.s3a.access.key', self.access_key)
        self.spark.conf.set('spark.hadoop.fs.s3a.secret.key', self.secret_key)
        self.spark.conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
        
        self.log4jLogger.info("Starting to read json data from S3 bucket...")
        s3_df = self.spark.read.json(f"{prefix}{self.BUCKET_NAME}/{self.LAYER_READ}/brewery_list.json")
        
        self.log4jLogger.info("Droping duplicates...")
        deduplication_df = s3_df.dropDuplicates()
        
        self.log4jLogger.info("Droping unnecessary columns...")
        drop_unnecessary_columns = deduplication_df.drop("address_1", "state_province")
        
        self.log4jLogger.info(" Writing data to S3 bucket...")
        drop_unnecessary_columns.write.partitionBy(["country", "state"]) \
            .mode("overwrite") \
            .parquet(f"{prefix}{self.BUCKET_NAME}/{self.LAYER_TYPE}/brewery.parquet")
