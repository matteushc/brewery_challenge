from unittest import TestCase, main
from plugins.extract_data_api import ExtractDataAPI
from unittest.mock import mock_open, patch
from airflow.sdk import ObjectStoragePath
from airflow.models import Connection
import os, json


class TestExtractDataAPI(TestCase):
    """
    This class contains methods to test the ExtractDataAPI class.
    It includes a method to get brewery data and save it to a file.
    """
    def setUp(self):
        self.api_url = "https://api.openbrewerydb.org/v1/breweries"
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default_value')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default_value')
        self.path_s3 = "s3://airflow-brewery-list/"
        self.layer = "bronze"
        self.extractor = ExtractDataAPI(self.api_url)


    def test_fetch_data(self):
        """
        Fetches brewery data from the API and saves it to a specified file path.
        """
        response = self.extractor.fetch_data()
        self.assertEqual(response.status_code, 200)
        list_brewery = response.json()
        self.assertIsInstance(list_brewery, list)
        
        
    def test_save_data_to_file(self):
        mock_file_handle = mock_open()
        import builtins
        
        with patch('builtins.open', mock_file_handle):
            data = 'Hello, world!'
            self.extractor.write_file(builtins, data)

            mock_file_handle().write.assert_called_once_with(data)


    def test_run_extractor(self):
        """
        Runs the extractor to fetch data and save it to a file.
        """
        ex = ExtractDataAPI(self.api_url)
        response = ex.fetch_data()
        
        conn = Connection(
            conn_id="aws-s3",
            conn_type="aws",
            login=self.access_key,
            password=self.secret_key,
            extra={
                "region_name": "us-east-1",
            },
        )
        env_key = f"AIRFLOW_CONN_{conn.conn_id.upper()}"
        conn_uri = conn.get_uri()
        os.environ[env_key] = conn_uri

        base = ObjectStoragePath(self.path_s3, conn_id="aws-s3")
        
        path = base / self.layer / f"brewery_list.json"
        json_string = json.dumps(response.json())
        json_bytes = json_string.encode('utf-8')
        ex.write_file(path, json_bytes)
        
        self.assertTrue(path.exists())


if __name__ == '__main__':
    main()
