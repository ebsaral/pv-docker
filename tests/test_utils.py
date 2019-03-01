from common.utils import *


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