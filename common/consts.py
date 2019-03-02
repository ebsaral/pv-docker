import datetime

import redis
from astral import Astral
from kombu import Exchange, Queue

DEBUG = False

RABBIT_URL = 'amqp://emin:123456@rabbitmq:5672/test'
EXCHANGE_NAME = 'test'
QUEUE_NAME = 'test'
ROUTING_KEY = "routing_test"
REDIS_HOST = 'redis'
CITY_NAME = 'Berlin' # Simulation daylight location

DEFAULT_START_HOUR = 4 # Simulation start hour (24)
DEFAULT_END_HOUR = 19 # Simulation end hour (24h)
DEFAULT_SHIFT_TIME_MIN = 20 # Next date in this seconds min during iteration
DEFAULT_SHIFT_TIME_MAX = 40 # Next date in this seconds max during iteration

DATE_FORMAT = '%m/%d/%Y'
DATETIME_FORMAT = '%m/%d/%Y, %H:%M:%S'

PREFIX = 'test-'


# Do not change the rest
redis_conn = redis.Redis(host=REDIS_HOST, port=6379, db=0)
exchange = Exchange(EXCHANGE_NAME, type='direct')
queues = [Queue(name=QUEUE_NAME, exchange=exchange, routing_key=ROUTING_KEY)]


def get_astral():
    astral = Astral()
    astral.solar_depression = 'civil'
    return astral

ASTRAL = get_astral()
ASTRAL_CITY = ASTRAL[CITY_NAME]

def get_sun(dt=None):
    if not dt:
        dt = datetime.datetime.today()
    return ASTRAL_CITY.sun(date=dt.date(), local=True)