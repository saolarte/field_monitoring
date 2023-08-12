import os
import sys
import time


import boto3
from dotenv import load_dotenv
from moto import mock_s3
import responses
from responses import matchers

from app import process
from test_cases import tests


# bucket_name = "test-bucket"
BUCKET_NAME = os.getenv("BUCKET_NAME")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.nasa.gov/planetary/earth/imagery"
CSV_FILE_NAME = "test_fields.csv"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(ROOT_DIR, CSV_FILE_NAME)



def prepare_api_mocks():
    for test in tests:
        test["params"]["api_key"] = API_KEY
        file_location = os.path.join(ROOT_DIR, test["file"])
        with open(file_location, "rb") as img1:
            responses.add(
                responses.GET,
                url=test["url"],
                status=200,
                body=img1.read(),
                content_type="image/png"

            )
        responses.add(
            responses.GET,
            url = BASE_URL,
            match = [matchers.query_param_matcher(test["params"])],
            json= {"img_url": test["url"]}
        )

def prepare_boto_mocks():
    s3_mock = mock_s3()
    s3_mock.start()
    s3_client = boto3.resource("s3")
    bucket = s3_client.Bucket(BUCKET_NAME)
    bucket.create()

@responses.activate
def run():
    prepare_api_mocks()
    prepare_boto_mocks()
    # s3_client = boto3.client("s3")
    s3_client = boto3.client("s3", 
                            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
                            aws_secret_access_key=os.getenv("S3_SECRET_KEY")
                            )
    process(s3_client, BUCKET_NAME, CSV_FILE_PATH)

if __name__ == "__main__":
    load_dotenv()
    run()