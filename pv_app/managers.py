from datetime import date

from common.utils import *


class PVCalculationManager():
    def __init__(self, timestamp, value, sun, panel_area=20):
        self._datetime = get_datetime_from_unix_timestamp(timestamp)
        self._timestamp = timestamp
        self._value = float(value)
        self._panel_area = panel_area
        self._pr = .75
        self._panel_efficiency = None
        self._sun = sun
        self._set_daylight()

    @classmethod
    def create(cls, key):
        timestamp, value = get_value_by_key(key)
        date = get_datetime_from_unix_timestamp(timestamp)
        pv_manager = cls(timestamp, value, get_sun(date))
        return pv_manager

    def _set_daylight(self):
        """
        Sets the dayligt boolean by comparing the given date
        :return:
        """
        if (self._sun['sunrise'] < self.datetime_value < self._sun['sunset']):
            self._daylight = True
        else:
            self._daylight = False

    def get_season(self):
        """
        Copied from internet. Gives the season from the date
        :return: str (season)
        """
        Y = self.datetime_value.date().year
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
        """
        Read-only
        :return: datetime (timestamp > date)
        """
        return self._datetime

    @property
    def timestamp(self):
        """
        Read-only
        :return: int (timestamp)
        """
        return self._timestamp

    @property
    def value(self):
        """
        Read-only
        :return: float (value)
        """
        return self._value

    @property
    def panel_area(self):
        """
        Read-only
        :return: float (Panel Area)
        """
        return self._panel_area

    @property
    def pr(self):
        """
        Read-only
        :return: float (Performance Ratio)
        """
        return self._pr

    @property
    def daylight(self):
        """
        Read-only
        :return: float (Panel Area)
        """
        return self._daylight

    @property
    def panel_efficiency_multiplier(self):
        """
        Return panel's efficiency % by deciding certain time intervals.
        Nothing scientific, this is an example
        :return: float (Panel Efficiency Multiplier)
        """
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
        """
        Decide a default value with the season and multiply it with the
        panel efficiency percentage
        :return: float
        """
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
        """
        Read only and cache mechanism
        :return: float (Panel efficiency value)
        """
        if not self._panel_efficiency:
            self._panel_efficiency = self.get_panel_efficiency_value()
        return self._panel_efficiency

    def _get_value_with_unit(self, is_mwh):
        """
        Concert the value according to its unit
        :param is_mwh: Bool
        :return: float (value or value / 1000)
        """
        return self.value if is_mwh else self.value / 1000

    def get_pv_value(self, is_mwh=True):
        """
        If there is no sunlight, then return 0.0
        Otherwise, apply the formula and return the result
        :param is_mwh: bool
        :return: float (PV Energy)
        """
        if not self.daylight:
            return 0.0
        value = self._get_value_with_unit(is_mwh)
        energy = self.panel_efficiency * self.panel_area * value * self.pr
        return energy

    def get_total(self, is_mwh):
        """
        Sum the pv value with the value with correct unit
        :param is_mwh: bool
        :return: float (pv_value + value)
        """
        pv_value = self.get_pv_value(is_mwh)
        return pv_value + self._get_value_with_unit(is_mwh)
