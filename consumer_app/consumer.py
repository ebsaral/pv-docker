import redis
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

from common.consts import (RABBIT_URL,
                           REDIS_HOST,
                           EXCHANGE_NAME,
                           QUEUE_NAME,
                           ROUTING_KEY)
from common.utils import format_message


class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        print(f'Consumer got the message: {body} and saved to Redis')
        r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
        t, v = format_message(body)
        r.append(t, v)
        message.ack()

exchange = Exchange(EXCHANGE_NAME, type="direct")
queues = [Queue(name=QUEUE_NAME, exchange=exchange, routing_key=ROUTING_KEY)]

if __name__ == '__main__':
    print(f'Consumer is listening {RABBIT_URL}')
    with Connection(RABBIT_URL, heartbeat=4) as conn:
        worker = Worker(conn, queues)
        worker.run()