import csv
from io import StringIO
import redis

from flask import Flask, render_template, make_response
from flask import request

from common.utils import *
from pv_app.managers import PVCalculationManager


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    keys = sorted(r.keys(f'{PREFIX}*'))
    sun = get_sun()

    if request.method == 'POST':
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['timestamp', 'date', 'is_daytime',
                     'value', 'pv_value', 'total_energy'])
        for key in keys:
            write_row_by_key(PVCalculationManager, r, cw, key, sun)
        output = make_response(si.getvalue())
        output.headers[
            "Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        r.flushall()
        return output
    else:
        counter = len(keys)
    return render_template('pv.html', counter=counter)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=DEBUG)