import logging
import os

from dotenv import load_dotenv
import requests


logging.basicConfig(level=logging.DEBUG)
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.nasa.gov/planetary/earth/imagery"


def make_request(longitude, latitude, dimension):
    parameters = {
        "lon": longitude,
        "lat": latitude,
        "dim": dimension,
        "api_key": API_KEY
    }
    response = requests.get(BASE_URL, params=parameters)
    if response.status_code == 200:
        return {"status": "ok"}
    else:
        logging.error(f"Error retrieving image: {response.status_code}")
        return {"status": "There was an error retrieven the image"}



