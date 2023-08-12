FROM python:3.9

RUN mkdir /app
COPY requirements.txt /app

WORKDIR "/app"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install cron -y

COPY . /app

RUN chmod 0644 /app/crontab
RUN /usr/bin/crontab  /app/crontab

CMD ["cron", "-f"]
