FROM python:3.7

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN mkdir app

RUN apt-get update -y && apt-get install -y python3-pip python-dev

COPY ./app ./app
COPY ./requirements.txt .
COPY ./app.py .

EXPOSE 5000

RUN pip install --upgrade pip && pip install -r requirements.txt
CMD python app.py

