import datetime
from datetime import date, datetime
from dateutil import tz
from pytz import timezone

from utils import get_datetime_from_unix_timestamp


class PVCalculationManager():
    def __init__(self, timestamp, value, sun, panel_area=20):
        self._datetime = get_datetime_from_unix_timestamp(timestamp)
        self._timestamp = timestamp
        self._value = float(value)
        self._panel_area = panel_area
        self._pr = .75
        self._panel_efficiency = None
        self._pv_value_mwh = None
        self._pv_value_kmw = None
        self._sun = sun
        self._set_daylight()

    def _set_daylight(self):
        if (self._sun['sunrise'] < self.datetime_value < self._sun['sunset']):
            self._daylight = True
        else:
            self._daylight = False

    def get_season(self):
        Y = self.datetime_value.date().year # dummy leap year to allow input X-02-29 (leap day)
        seasons = [('winter', (date(Y, 1, 1), date(Y, 3, 20))),
                   ('spring', (date(Y, 3, 21), date(Y, 6, 20))),
                   ('summer', (date(Y, 6, 21), date(Y, 9, 22))),
                   ('autumn', (date(Y, 9, 23), date(Y, 12, 20))),
                   ('winter', (date(Y, 12, 21), date(Y, 12, 31)))]


        now = self.datetime_value.date()
        now = now.replace(year=Y)
        return next(season for season, (start, end) in seasons
                    if start <= now <= end)
    @property
    def datetime_value(self):
        return self._datetime.astimezone(timezone('utc')).replace(
            microsecond=0)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def value(self):
        return self._value

    @property
    def panel_area(self):
        return self._panel_area

    @property
    def pr(self):
        return self._pr

    @property
    def daylight(self):
        return self._daylight

    @property
    def panel_efficiency_multiplier(self):
        hour = self.datetime_value.hour
        if hour in range(6, 8):
            return 30.0
        elif hour in range(8, 10):
            return 40.0
        elif hour in range(10, 12):
            return 60.0
        elif hour in range(12, 14):
            return 70.0
        elif hour in range(14, 16):
            return 80.0
        elif hour in range(16, 18):
            return 90.0
        else:
            return 70.0

    def get_panel_efficiency_value(self):
        season = self.get_season()
        m = self.panel_efficiency_multiplier
        if season == 'winter':
            return 0.30 * m
        elif season == 'spring':
            return 0.70 * m
        elif season == 'autumn':
            return 0.60 * m
        elif season == 'summer':
            return 0.90 * m
        return 0

    @property
    def panel_efficiency(self):
        if not self._panel_efficiency:
            self._panel_efficiency = self.get_panel_efficiency_value()
        return self._panel_efficiency

    def _get_value_with_unit(self, is_mwh):
        return self.value if is_mwh else self.value / 1000

    def get_pv_value(self, is_mwh=True):
        if not self.daylight:
            return 0.0
        value = self._get_value_with_unit(is_mwh)
        energy = self.panel_efficiency * self.panel_area * value * self.pr
        return energy

    def get_total(self, is_mwh):
        pv_value = self.get_pv_value(is_mwh)
        return pv_value + self._get_value_with_unit(is_mwh)
