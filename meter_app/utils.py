from kombu import Connection
from kombu.mixins import ConsumerProducerMixin

from common.utils import *


class Worker(ConsumerProducerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    @classmethod
    def push_data(cls, data):
        with Connection(RABBIT_URL, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            for data_tuple in data:
                worker.handle_message(format_data(data_tuple))

    def handle_message(self, message):
        self.producer.publish(
            message,
            exchange=exchange,
            routing_key=ROUTING_KEY,
            retry=True,
        )