"""This module defines a class to process a JSON file from an S3 bucket using PySpark.
"""
import os
from pyspark.sql import SparkSession


class SaveGoldLayer:

    BUCKET_NAME = "airflow-data-create"
    LAYER_READ = "silver"
    LAYER_TYPE = "gold"


    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default_value')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default_value')
        
        self.log4jLogger = spark._jvm.org.apache.log4j.LogManager.getLogger(__name__)


    def process(self):
        
        self.spark.conf.set('spark.hadoop.fs.s3a.access.key', self.access_key)
        self.spark.conf.set('spark.hadoop.fs.s3a.secret.key', self.secret_key)
        self.spark.conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
        
        self.log4jLogger.info("Starting to read parquet data from S3 bucket...")
        s3_df = self.spark.read.parquet(f"s3a://{self.BUCKET_NAME}/{self.LAYER_READ}/brewery.parquet")
        
        self.log4jLogger.info(s3_df.printSchema())

        self.log4jLogger.info("Transforming data making a group by columns brewery_type and city...")
        transformed_df = s3_df.groupBy(["brewery_type", "city"]) \
            .count().withColumnRenamed("count", "total")
            
        self.log4jLogger.info(transformed_df.show())
        
        self.log4jLogger.info(f"Writing transformed data back to S3 bucket: s3a://{self.BUCKET_NAME}/{self.LAYER_TYPE}/...")
        transformed_df.write \
            .mode("overwrite") \
            .parquet(f"s3a://{self.BUCKET_NAME}/{self.LAYER_TYPE}/brewery.parquet")
