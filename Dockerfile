FROM python:3.9.5

WORKDIR /usr/src/app

# Install dependencies
RUN apt install git && \
    pip install tb-mqtt-client && \
    git clone https://github.com/RuXBee/upna-iot-parking.git && \
    cd upna-iot-parking && \
    git checkout develop

RUN apt-get update -y 

CMD [ "python", "-u", "upna-iot-parking/main.py" ]

