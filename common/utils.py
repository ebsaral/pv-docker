import calendar
import csv
import random
from io import StringIO

from flask import make_response

from pytz import timezone

from common.consts import *


def get_datetime():
    return datetime.datetime.now().astimezone(timezone('utc')).replace(
        microsecond=0)

def get_timestamp(dt):
    return calendar.timegm(dt.timetuple())

def randomly_increase_datetime_by_seconds(dt, seconds):
    return dt + datetime.timedelta(seconds=seconds)

def get_random_watt_value(min_limit=0, max_limit=9000):
    value = random.randint(min_limit, max_limit)
    return value

def get_begin_and_end_datetime(dt):
    min_datetime = datetime.datetime.combine(
        dt.date(), datetime.time.min)
    max_datetime = datetime.datetime.combine(
        dt.date(), datetime.time.max)
    return min_datetime, max_datetime

def get_populated_data(start_hour=DEFAULT_START_HOUR,
                       end_hour=DEFAULT_END_HOUR,
                       jump_min=DEFAULT_SHIFT_TIME_MIN,
                       jump_max=DEFAULT_SHIFT_TIME_MAX,
                       custom_date=None):
    today_datetime = custom_date if custom_date else get_datetime()
    today_begin_datetime, today_end_datetime = get_begin_and_end_datetime(
        today_datetime
    )

    current_time = today_begin_datetime.replace(hour=start_hour)
    while current_time.hour >= start_hour and current_time.hour < end_hour:
        timestamp = get_timestamp(current_time)
        value = get_random_watt_value()
        yield (timestamp, value)
        jump = random.randint(jump_min, jump_max)
        current_time = randomly_increase_datetime_by_seconds(
            current_time, seconds=jump)


def format_data(data_tuple):
    return {'timestamp': data_tuple[0], 'value': data_tuple[1]}

def format_message(message):
    timestamp = str(message.get("timestamp"))
    value = int(message.get("value"))
    return f'{PREFIX}{timestamp}', value

def get_datetime_from_unix_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).astimezone(
        timezone('utc'))

def get_value_by_key(key):
    timestamp = int(key.decode('utf8').lstrip(PREFIX))
    value = int(redis_conn.get(key).decode('utf8'))
    return timestamp, value

def get_csv_fields():
    fields = ['timestamp', 'date', 'is_daytime', 'value',
              'pv_value', 'total_energy']
    return fields

def get_csv_data(pv_manager):
    date = pv_manager.datetime_value.strftime(DATETIME_FORMAT)
    pv_value = pv_manager.get_pv_value(is_mwh=False)
    total = pv_manager.get_total(is_mwh=False)

    data = {
        'timestamp': pv_manager.timestamp,
        'date': date,
        'is_daytime': pv_manager.daylight,
        'value': pv_manager.value,
        'pv_value': pv_value,
        'total_energy': total
    }

    return data

def get_redis_keys():
    keys = sorted(redis_conn.keys(f'{PREFIX}*'))
    return keys


def create_csv(data, filename):
    si = StringIO()
    cw = csv.DictWriter(si, fieldnames=get_csv_fields())

    cw.writeheader()

    for d in data:
        cw.writerow(d)

    output = make_response(si.getvalue())
    output.headers[
        "Content-Disposition"] = f"attachment; filename={filename}"
    output.headers["Content-type"] = "text/csv"
    return output