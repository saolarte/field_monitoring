import sys
import os
import json
import unittest

import boto3
from dotenv import load_dotenv
from moto import mock_s3
import responses
from responses import matchers


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from field_monitoring.app import make_request, read_csv, upload_file_to_s3

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.nasa.gov/planetary/earth/imagery"
FILE_NAME = "test_fields.csv"
FILE_LOCATION = os.path.join(ROOT_DIR, FILE_NAME)

load_dotenv()

class TestMakeRequest(unittest.TestCase):

    @responses.activate
    def test_200(self):
        params = {
            "lon": 100.71,
            "lat": 1.5,
            "dim": 0.030,
            "api_key": API_KEY
        }
        responses.add(
            responses.GET,
            url = BASE_URL,
            match = [matchers.query_param_matcher(params)],
            json= {"img_url": "https://mundogeo.com/wp-content/uploads/2022/02/23142632/pleiades-satellite-image-902x400.jpg"}
        )

        response = make_request(
            longitude=params["lon"],
            latitude=params["lat"],
            dimension=params["dim"]
        )
        
        assert response["status"] == "ok"
        assert "image" in response.keys()

    @responses.activate
    def test_401(self):
        params = {
            "lon": 100.72,
            "lat": 1.5,
            "dim": 0.030,
            "api_key": API_KEY
        }
        responses.add(
            responses.GET,
            url = BASE_URL,
            match = [matchers.query_param_matcher(params)],
            status=401,
            body=""
        )

        response = make_request(
            longitude=params["lon"],
            latitude=params["lat"],
            dimension=params["dim"]
        )
        
        assert "error" in response["status"]


class TestReadCsv(unittest.TestCase):
    def test_ok(self):
        fields = read_csv(FILE_LOCATION)
        assert fields[0]["lat"] == "100.71"
        assert fields[1]["lat"] == "100.72"
        assert fields[2]["lat"] == "100.73"

class TestUploadFile(unittest.TestCase):

    bucket_name = "test-bucket"
    def setUp(self):
        self.mock_s3 = mock_s3()
        self.mock_s3.start()

        s3_client = boto3.resource("s3")
        bucket = s3_client.Bucket(self.bucket_name)
        bucket.create()

    def tearDown(self):
        self.mock_s3.stop()

    def test_ok(self):
        s3_client = boto3.client("s3")

        file_name = "test_1.jpg"
        file_url = f"test_images/{file_name}"
        field_data = {"field_id": "field_2"}
        
        result = upload_file_to_s3(s3_client, file_url, field_data, bucket=self.bucket_name)

        assert "imagery.png" in result
    



    

