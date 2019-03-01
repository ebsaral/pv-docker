# pv-docker
PV simulator example

## Local Simulation Environment

`docker-compose up`

`http://localhost:5000` -> Where you hit the populate button, and simulate consumption throughout the day. Send messages to RabbitMQ broker. Same page gives you the total number of data populated after hitting the button.

When the messages get pushed to RabbitMQ, another consumer app listens to the queue and writes the collected data into Redis.

`http://localhost:5001` -> Where you retrieve messages from Redis (cache method) and export as csv after applying PV simulator algorithm. Same page displays the number of items waiting in Redis database to be exported (hit refresh). 


## Tests

`virtualenv env -p python3`

`source env/bin/activate`

`pip install -r requirements.txt`

`pytest`


## Note

This project can easily be construct into three-microservices structure: Meter App, PV App (Consumer + Export) and RabbitMQ app.
