import redis
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

from consts import RABBIT_URL
from utils import format_message


class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        print(body)
        r = redis.Redis(host='redis', port=6379, db=0)
        t, v = format_message(body)
        r.append(t, v)
        message.ack()

exchange = Exchange("test", type="direct")
queues = [Queue(name="test", exchange=exchange, routing_key="MM")]

if __name__ == '__main__':
    with Connection(RABBIT_URL, heartbeat=4) as conn:
        worker = Worker(conn, queues)
        worker.run()