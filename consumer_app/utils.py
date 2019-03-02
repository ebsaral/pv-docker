from kombu import Connection
from kombu.mixins import ConsumerMixin

from common.utils import *


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

    @classmethod
    def consume_data(cls):
        with Connection(RABBIT_URL, heartbeat=4) as conn:
            worker = cls(conn, queues)
            worker.run()