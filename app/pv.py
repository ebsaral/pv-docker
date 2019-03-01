import csv
import datetime
from io import StringIO
import redis

from flask import Flask, render_template, make_response
from flask import request

from utils import get_sun, write_row_by_key
from managers import PVCalculationManager

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    r = redis.Redis(host='redis', port=6379, db=0)
    keys = sorted(r.keys('test-*'))
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
    app.run(host='0.0.0.0', debug=True)