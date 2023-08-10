import os
import json
import unittest

from dotenv import load_dotenv
import responses
from responses import matchers

from app import make_request

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.nasa.gov/planetary/earth/imagery"


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
            body="test"
        )

        response = make_request(
            longitude=params["lon"],
            latitude=params["lat"],
            dimension=params["dim"]
        )
        
        assert response["status"] == "ok"

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
