DEBUG = False

RABBIT_URL = "amqp://emin:123456@rabbitmq:5672/test"
EXCHANGE_NAME = "test"
QUEUE_NAME = "test"
ROUTING_KEY = "routing_test"

REDIS_HOST = "redis"

CITY_NAME = "Berlin" # Simulation daylight location

DEFAULT_START_HOUR = 4 # Simulation start hour (24)
DEFAULT_END_HOUR = 19 # Simulation end hour (24h)
DEFAULT_SHIFT_TIME_MIN = 20 # Next date in this seconds min during iteration
DEFAULT_SHIFT_TIME_MAX = 40 # Next date in this seconds max during iteration

PREFIX = "test-"