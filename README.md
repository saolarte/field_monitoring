# field_monitoring

Simple application that retrieves images from NASA's Earth API and stores them in AWS S3

A CSV file is expected as input for the app, which provides field_id, longitude, latitude and dimension.


## Run the app
### Locally
Install dependencies:
```
pip install pipenv
pipenv install -r requirements.txt
```

Run the script:
```
python run_app.py
```


### Docker container

Build and run the container:
```
docker build -t field_monitoring .
docker run -d field_monitoring
```
Log in to the container in interactive mode to check the logs:
```
docker exec -it <container_id>
Use the output of the run command as container_id
```

Logs from the process are being stored in /app/cron.log
```
cat /app/cron.log
```

The process is set to run once every minute, for testing purposes, by using crontab.
This setting can be changed from the crontab file located in the project root.


## Run tests

Tests can be ran using the following command:
```
pytest
```
API calls to NASA's API are mocked using responses library (See docs [here](https://pypi.org/project/responses/))

Calls to AWS S3 service are mocked using moto (See docs [here](https://docs.getmoto.org))
