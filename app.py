import csv
from datetime import date
import logging
import os

import boto3
from dotenv import load_dotenv
import requests


logging.basicConfig(level=logging.DEBUG)
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.nasa.gov/planetary/earth/imagery"
BUCKET_NAME = "test-bucket-san9405"
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")




def make_request(field_data):
    parameters = {
        "lon": field_data["lon"],
        "lat": field_data["lat"],
        "dim": field_data["dim"],
        "api_key": API_KEY
    }
    response = requests.get(BASE_URL, params=parameters)
    if response.status_code == 200:
        return {"status": "ok", "image": response.json().get("img_url")}
    else:
        logging.error(f"Error retrieving image: {response.status_code}")
        return {"status": "There was an error retrieven the image"}


def read_csv(file_location):
    with open(file_location) as file:
        csv_reader = csv.DictReader(file)
        fields = [row for row in csv_reader]
    return fields


def upload_file_to_s3(s3_client, file_object, field_data, bucket=BUCKET_NAME):
    today = date.today()
    file_destination = f"{field_data['field_id']}/{today.strftime('%Y%m%d')}_imagery.png"
    try:
        response = s3_client.upload_fileobj(file_object, bucket, file_destination)
    except Exception as error:
        logging.error(f"Error uploading file to S3: {str(error)}")
        return False
    return file_destination
    


def process_images(s3_client, bucket):
    fields = read_csv("test_fields.csv")
    for field in fields:
        response = make_request(field)
        if response["status"] == "ok":
            img = requests.get(
                response["image"],
                stream=True
            )
            upload_response = upload_file_to_s3(s3_client, img.raw, field, bucket)



            
            

