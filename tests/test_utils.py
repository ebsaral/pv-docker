from unittest import mock

import pytest

from astral import Location

from common.utils import *
from pv_app.managers import PVCalculationManager


def test_get_datetime():
    dt = datetime.datetime.now().astimezone(timezone('utc')).replace(
        microsecond=0)
    expected_dt = get_datetime()
    assert dt == expected_dt


def test_get_timestamp():
    dt = datetime.datetime.now().astimezone(timezone('utc')).replace(
        microsecond=0)
    expected = calendar.timegm(dt.timetuple())
    data = get_timestamp(dt)
    assert data == expected


def test_randomly_increase_datetime_by_seconds():
    dt = datetime.datetime.now()
    seconds = 15
    data = randomly_increase_datetime_by_seconds(dt, seconds)
    expected = dt + datetime.timedelta(seconds=seconds)
    assert data == expected


def test_get_random_watt_value(monkeypatch):
    def mock_random_value(a, b):
        return 10
    monkeypatch.setattr(random, 'randint', mock_random_value)
    x = get_random_watt_value()
    assert x == 10


def test_get_begin_and_end_datetime():
    dt = datetime.datetime.now()

    min_expected = datetime.datetime.combine(
        dt.date(), datetime.time.min)
    max_expected = datetime.datetime.combine(
        dt.date(), datetime.time.max)

    min_data, max_data = get_begin_and_end_datetime(dt)

    assert min_data == min_expected
    assert max_expected == max_data


def test_format_data():
    data = (123, 456)
    expected_data = {'timestamp': data[0], 'value': data[1]}
    formatted_data = format_data(data)
    assert  expected_data == formatted_data


def test_format_message():
    data = {'timestamp': 123, 'value': 456}
    timestamp = data.get('timestamp')
    expected_value = data.get('value')
    expected_message = f'test-{timestamp}'
    formatted_message, formatted_value = format_message(data)

    assert expected_value == formatted_value
    assert expected_message == formatted_message


def test_get_datetime_from_unix_timestamp():
    expected_dt = datetime.datetime.now().astimezone(timezone('utc')).replace(
        microsecond=0)
    timestamp = calendar.timegm(expected_dt.timetuple())
    dt = get_datetime_from_unix_timestamp(timestamp)
    assert expected_dt == dt

def test_get_astral():
    astral = get_astral()
    assert isinstance(astral, Astral)

def test_get_astral_city():
    astral = get_astral()
    assert isinstance(astral, Astral)
    city = get_astral_city(astral)
    assert isinstance(city, Location)
    assert CITY_NAME.lower() in city.name.lower()


@pytest.mark.freeze_time('2019-03-01')
def test_get_sun():
    sun = get_sun()
    assert type(sun) == dict

    assert 'dawn' in sun
    assert 'sunrise' in sun


def test_get_values_by_key(monkeypatch):
    redis = mock.Mock()

    def redis_mock(key):
        return b'1234'
    monkeypatch.setattr(redis, 'get', redis_mock)

    dt = get_datetime()
    ts = get_timestamp(dt)

    timestamp, value = get_values_by_key(redis, f"{ts}".encode('utf8'))

    assert timestamp == ts
    assert value == 1234


def test_construct_row():
    row = construct_row(1, 2, 3, 4, 5, 6)
    assert  row == [1, 2, 3, 4, 5, 6]

def test_get_manager():
    redis = mock.Mock()
    sun = get_sun()
    key = f"{PREFIX}123456".encode('utf8')

    def redis_get_mock(key):
        return b'1234'

    redis.get = redis_get_mock
    manager = get_manager(redis, key, sun)
    assert isinstance(manager, PVCalculationManager)

    assert manager.timestamp == 123456
    assert manager.value == 1234


@pytest.mark.freeze_time('2019-03-01 12:00:00+0000')
def test_write_row_by_key():
    manager = mock.Mock()
    cw = mock.Mock()
    ts = str(get_timestamp(get_datetime()))
    value = 1234

    def cv_mock(row):
        return True

    def get_pv_value_mock(is_mwh):
        return 2345

    def get_total_mock(is_mwh):
        return 1000

    def format_date(format):
        return get_datetime().strftime(format)

    cw.writerow = cv_mock
    manager.get_total = get_total_mock
    manager.get_pv_value = get_pv_value_mock
    manager.datetime_value.strftime = format_date
    manager.timestamp = int(ts)
    manager.daylight = True
    manager.value = value

    row = write_row_by_key(manager, cw)
    date = get_datetime().strftime("%m/%d/%Y, %H:%M:%S")
    expected_row = [int(ts), date, True, 1234, 2345, 1000]

    assert row == expected_row

@pytest.mark.freeze_time('2019-03-01 12:00:00+0000')
def test_populate_data(monkeypatch, mocker):

    dt = get_datetime()
    value = 10000

    def get_random_watt_value_mock():
        return value

    mocker.patch('common.utils.get_random_watt_value',
                 get_random_watt_value_mock)

    data = populate_data(10, 11, 20, 20)
    begin, end = get_begin_and_end_datetime(dt)

    expected_data = []
    current_time = begin.replace(hour=10)
    while current_time.hour >= 10 and current_time.hour < 11:
        timestamp = get_timestamp(current_time)
        expected_data.append((timestamp, value))
        current_time = randomly_increase_datetime_by_seconds(
            current_time, seconds=20)

    assert data == expected_data