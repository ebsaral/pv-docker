import calendar
import datetime
import random

from astral import Astral
from pytz import timezone

PREFIX = 'test-'

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

def populate_data(start_hour=4, end_hour=19, jump_min=20, jump_max=40):
    today_datetime = get_datetime()
    today_begin_datetime, today_end_datetime = get_begin_and_end_datetime(
        today_datetime
    )

    jump = random.randint(jump_min, jump_max)

    data = []
    current_time = today_begin_datetime.replace(hour=start_hour)
    while current_time.hour >= start_hour and current_time.hour < end_hour:
        timestamp = get_timestamp(current_time)
        value = get_random_watt_value()
        data.append((timestamp, value))
        current_time = randomly_increase_datetime_by_seconds(
            current_time, seconds=jump)

    return data

def format_data(data_tuple):
    return {'timestamp': data_tuple[0], 'value': data_tuple[1]}

def format_message(message):
    timestamp = str(message.get("timestamp"))
    value = int(message.get("value"))
    return f'{PREFIX}{timestamp}', value

def get_datetime_from_unix_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).astimezone(
        timezone('utc'))

def get_sun():
    astral = Astral()
    city_name = 'Berlin'
    astral.solar_depression = 'civil'
    city = astral[city_name]
    datetime_value = datetime.datetime.today()
    sun = city.sun(date=datetime_value.date(), local=True)
    return sun

def get_values_by_key(redis, key):
    timestamp = int(key.decode('utf8').lstrip(PREFIX))
    value = int(redis.get(key).decode('utf8'))
    return timestamp, value

def write_row_by_key(manager, redis, cw, key, sun):
    timestamp, value = get_values_by_key(redis, key)
    pv_manager = manager(timestamp, value, sun)
    pv_value = pv_manager.get_pv_value(is_mwh=False)
    total = pv_manager.get_total(is_mwh=False)
    date = pv_manager.datetime_value.strftime("%m/%d/%Y, %H:%M:%S")
    is_daytime = pv_manager.daylight
    cw.writerow([timestamp, date, is_daytime, value, pv_value, total])
