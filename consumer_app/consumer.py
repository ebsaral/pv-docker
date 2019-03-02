from consumer_app.utils import Worker

from common.consts import RABBIT_URL


if __name__ == '__main__':
    print(f'Consumer is listening {RABBIT_URL}')
    Worker.consume_data()