"""This module defines the ExtractDataAPI class, which is responsible for fetching data from a specified API and saving it to a file.
"""
import requests
import json
from airflow.sdk import ObjectStoragePath
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ExtractDataAPI:
    
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response
    
    def convert_to_bytes(self, response):
        json_string = json.dumps(response.json())
        json_bytes = json_string.encode('utf-8')
        return json_bytes
    
    def write_file(self, path: ObjectStoragePath, content: str):
        with path.open("wb") as f:
            f.write(content)
