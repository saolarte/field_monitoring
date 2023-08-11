# field_monitoring

Simple application that retrieves images from NASA's Earth API and stores them in AWS S3

A CSV file is expected as input for the app, which provides field_id, longitude, latitude and dimension.

## Run tests

Tests can be ran using the following command:
```
pytest
```
API calls to NASA's API are mocked using responses library (See docs [here](https://pypi.org/project/responses/))

Calls to AWS S3 service are mocked using moto (See docs [here](https://docs.getmoto.org))
