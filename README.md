# pv-docker
PV simulator example

[![CodeCov](https://codecov.io/gh/ebsaral/pv-docker/branch/master/graph/badge.svg)](https://codecov.io/gh/ebsaral/pv-docker)

[![CircleCI](https://circleci.com/gh/ebsaral/pv-docker/tree/master.svg?style=svg)](https://circleci.com/gh/ebsaral/pv-docker/tree/master)

## Local Simulation Environment

If you want to change settings, please have a look at `common/consts.py` and `docker-compose.yml`

### Run

`docker-compose up` *suggested*

or specifically:

`docker-compose up [rabbitmq|consumer|redis|meter|pv]`

Wait until RabbitMQ Server is running but that shouldn't be a problem as well. 

### Meter Service

`http://localhost:5000`: Where you hit the populate button, and simulate consumption throughout the day. Send messages to RabbitMQ broker. Same page gives you the total number of data populated after hitting the button. Check the container: `meter`

### Consumer Service

When the messages get pushed to RabbitMQ, another consumer app listens to the queue and writes the collected data into Redis. Check the container `consumer`

### PV Service

The applied formula: `E = A * r  * H * PR`

E: Energy (kWh)

A: Total solar panel area (m2)

r: Solar panel yield of efficiency

H: Annual average solar radiation on tilted panels (meter input)

PR: Performance ratio, coefficient for losses (default: .75)

`http://localhost:5001` -> Where you retrieve messages from Redis (cache method) and export as csv after applying PV simulator manager (`pv_app.managers.PVCalculationManager`). Same page displays the number of items waiting in Redis database to be exported if you click on refresh. After the export, the redis database gets flushed. 

### RabbitMQ Service

Works as the message broker. Check the container `rabbitmq`


## Tests

`virtualenv env -p python3`

`source env/bin/activate`

`pip install -r requirements/test.txt`

`pytest`

or 

`docker compose up test`

## Note

This project can easily be construct into three-microservices structure: Meter App, PV App (Consumer + Export) and RabbitMQ app.
