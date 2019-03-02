from flask import Flask, render_template, jsonify

from common.utils import *
from pv_app.managers import PVCalculationManager
from pv_app.utils import nocache

app = Flask(__name__)


@app.route('/count', methods=['GET'])
def count():
    data = {'count': len(get_redis_keys())}
    return jsonify(data)


@app.route('/flush', methods=['GET'])
def flush():
    redis_conn.flushall()
    return jsonify({'success': True})


@app.route('/export', methods=['GET'])
@nocache
def export():
    keys = get_redis_keys()

    data = []
    for key in keys:
        manager = PVCalculationManager.create(key)
        data.append(get_csv_data(manager))

    date = get_datetime().date().strftime(DATE_FORMAT)
    return create_csv(data, filename=f'pv-docker-data-{date}.csv')


@app.route('/', methods=['POST', 'GET'])
def main():
    counter = len(get_redis_keys())
    return render_template('pv.html', counter=counter)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=DEBUG)