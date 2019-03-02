from flask import Flask, render_template
from flask import request

from meter_app.utils import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'X1234567!'

@app.route('/', methods=['POST', 'GET'])
def main():
    counter, data, date = None, None, None
    today_str = get_datetime().strftime(DATE_FORMAT)

    if request.method == 'POST':
        date_str = request.form.get('date') or today_str
        date = datetime.datetime.strptime(date_str, DATE_FORMAT)
        data = list(get_populated_data(custom_date=date))
        counter = str(len(data))
        Worker.push_data(data)

    return render_template('meter.html',
                           counter=counter,
                           data=data,
                           now=date or get_datetime())

if __name__ == '__main__':
    app.run('0.0.0.0', debug=DEBUG)