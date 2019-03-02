import pytest

from pv_app.managers import PVCalculationManager

from common.utils import *


def get_manager_and_timestamp_for_test():
    ts = get_timestamp(get_datetime())
    manager = PVCalculationManager(timestamp=ts, value=1000, sun=get_sun())
    return manager, ts


@pytest.mark.freeze_time('2019-09-01 12:00:00+0200')
def test_pvcalculation_init_daylight_true():
    manager, ts = get_manager_and_timestamp_for_test()

    dt = get_datetime_from_unix_timestamp(ts)

    assert dt == get_datetime()
    assert manager.datetime_value == dt
    assert manager.timestamp == ts
    assert manager.value == 1000
    assert manager.daylight == True


@pytest.mark.freeze_time('2019-03-01 2:00:00+0200')
def test_pvcalculation_init_daylight_false():
    manager, ts = get_manager_and_timestamp_for_test()

    dt = get_datetime_from_unix_timestamp(ts)

    assert dt == get_datetime()
    assert manager.timestamp == ts
    assert manager.value == 1000
    assert manager.daylight == False


@pytest.mark.freeze_time('2019-03-01 12:00:00+0200')
def test_pvcalculation_get_season_winter():
    manager, ts = get_manager_and_timestamp_for_test()

    dt = get_datetime()
    ts = get_timestamp(dt)

    assert manager.timestamp == ts
    assert manager.value == 1000
    assert manager.daylight == True
    assert manager.get_season() == 'winter'


@pytest.mark.freeze_time('2019-04-01 12:00:00+0200')
def test_pvcalculation_get_season_spring():
    manager, ts = get_manager_and_timestamp_for_test()

    dt = get_datetime()
    ts = get_timestamp(dt)

    assert manager.timestamp == ts
    assert manager.value == 1000
    assert manager.daylight == True
    assert manager.get_season() == 'spring'


@pytest.mark.freeze_time('2019-07-01 12:00:00+0200')
def test_pvcalculation_get_season_summer():
    manager, ts = get_manager_and_timestamp_for_test()

    dt = get_datetime()
    ts = get_timestamp(dt)

    assert manager.timestamp == ts
    assert manager.value == 1000
    assert manager.daylight == True
    assert manager.get_season() == 'summer'


@pytest.mark.freeze_time('2019-10-01 12:00:00+0200')
def test_pvcalculation_get_season_autumn():
    manager, ts = get_manager_and_timestamp_for_test()

    dt = get_datetime()
    ts = get_timestamp(dt)

    assert manager.timestamp == ts
    assert manager.value == 1000
    assert manager.daylight == True
    assert manager.get_season() == 'autumn'


def test_pvcalculation_panel_area():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.panel_area == 20


def test_pvcalculation_datetime_value():
    manager, ts = get_manager_and_timestamp_for_test()
    dt = get_datetime()
    assert manager.datetime_value == dt


def test_pvcalculation_timestamp():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.timestamp == ts


def test_pvcalculation_value():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.value == 1000


def test_pvcalculation_pr():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.pr == .75


@pytest.mark.freeze_time('2019-07-01 08:00:00+0200')
def test_pvcalculation_panel_efficiency_multiplier_30():
    manager, ts = get_manager_and_timestamp_for_test()
    dt = get_datetime()
    assert dt.hour == manager.datetime_value.hour
    assert manager.panel_efficiency_multiplier == 30

@pytest.mark.freeze_time('2019-07-01 10:00:00+0200')
def test_pvcalculation_panel_efficiency_multiplier_40():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.panel_efficiency_multiplier == 40


@pytest.mark.freeze_time('2019-07-01 12:00:00+0200')
def test_pvcalculation_panel_efficiency_multiplier_60():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.panel_efficiency_multiplier == 60


@pytest.mark.freeze_time('2019-07-01 14:00:00+0200')
def test_pvcalculation_panel_efficiency_multiplier_70():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.panel_efficiency_multiplier == 70


@pytest.mark.freeze_time('2019-07-01 16:00:00+0200')
def test_pvcalculation_panel_efficiency_multiplier_80():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.panel_efficiency_multiplier == 80


@pytest.mark.freeze_time('2019-07-01 18:00:00+0200')
def test_pvcalculation_panel_efficiency_multiplier_90():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.panel_efficiency_multiplier == 90


@pytest.mark.freeze_time('2019-03-01 18:00:00+0200')
def test_pvcalculation_get_panel_efficiency_value_winter():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.get_panel_efficiency_value() == 90 * .30


@pytest.mark.freeze_time('2019-07-01 12:00:00+0200')
def test_pvcalculation_get_panel_efficiency_value_summer():
    manager, ts = get_manager_and_timestamp_for_test()
    assert manager.get_panel_efficiency_value() == 60 * .90
