FROM python:3.9.5

WORKDIR /usr/src/app

COPY ./src .

EXPOSE 1883

# Install dependencies
RUN apt install git \
    && pip install tb-mqtt-client

RUN apt-get update -y 

CMD [ "python", "-u", "/usr/src/app/main.py" ]

