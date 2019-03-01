from flask import Flask, render_template
from flask import request

from consts import RABBIT_URL
from utils import populate_data, format_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'X1234567!'

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerProducerMixin

exchange = Exchange("test", type="direct")
queues = [Queue(name="test", exchange=exchange, routing_key="MM")]


class Worker(ConsumerProducerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=Queue('foo'),
                         on_message=self.handle_message,
                         accept='application/json',
                         prefetch_count=10)]

    def handle_message(self, message):
        self.producer.publish(
            message,
            exchange=exchange,
            routing_key='MM',
            retry=True,
        )


@app.route('/', methods=['POST', 'GET'])
def main():
    counter = None
    if request.method == 'POST':
        data = populate_data()
        counter = str(len(data))
        with Connection(RABBIT_URL, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            for data_tuple in data:
                worker.handle_message(format_data(data_tuple))

    return render_template('index.html', counter=counter)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)