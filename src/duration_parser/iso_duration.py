from __future__ import annotations

import re
from decimal import Decimal

from . import calendar
from .exceptions import IncorrectDesignator, IncorrectNumber, IncorrectPattern
from .util import convert_to_dict, rename

ISO8601_PERIOD_REGEX = re.compile(
    r"^(?P<sign>[+-])?"
    r"P(?!\b)"
    r"(?P<years>[0-9]+([0-9]+)?Y)?"
    r"(?P<months>[0-9]+([0-9]+)?M)?"
    r"(?P<days>[0-9]+([0-9]+)?D)?"
    r"((?P<separator>T)(?P<hours>[0-9]+([0-9]+)?H)?"
    r"(?P<minutes>[0-9]+([0-9]+)?M)?"
    r"(?P<seconds>[0-9]+([0-9]+)?S)?"
    r"(?P<miliseconds>[0-9]+([0-9]+)?m)?"
    r"(?P<microseconds>[0-9]+([0-9]+)?u)?"
    r"(?P<nanoseconds>[0-9]+([0-9]+)?n)?)?$"
)


class ISODuration(object):
    date_map_dict = {"years": "Y", "months": "M", "days": "D"}

    time_map_dict = {
        "hours": "H",
        "minutes": "M",
        "seconds": "S",
        "miliseconds": "m",
        "microseconds": "u",
        "nanoseconds": "n",
    }

    def __init__(self):
        self.years: int = 0
        self.months: int = 0
        self.days: int = 0
        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0
        self.miliseconds: int = 0
        self.microseconds: int = 0
        self.nanoseconds: int = 0

    @staticmethod
    def _wrap(duration_dict: dict) -> ISODuration:
        iso_duration = ISODuration()
        iso_duration.years = duration_dict.get("pY", 0)
        iso_duration.months = duration_dict.get("pM", 0)
        iso_duration.days = duration_dict.get("pD", 0)
        iso_duration.hours = duration_dict.get("tH", 0)
        iso_duration.minutes = duration_dict.get("tM", 0)
        iso_duration.seconds = duration_dict.get("tS", 0)
        iso_duration.miliseconds = duration_dict.get("tm", 0)
        iso_duration.microseconds = duration_dict.get("tu", 0)
        iso_duration.nanoseconds = duration_dict.get("tn", 0)
        return iso_duration

    def get_seconds(self) -> Decimal:
        days_seconds = (
            self.years * calendar.SECONDS_IN_YEAR
            + self.months * calendar.SECONDS_IN_MONTH
            + self.days * calendar.SECONDS_IN_DAY
            + self.hours * calendar.SECONDS_IN_HOUR
            + self.minutes * calendar.SECONDS_IN_MINUTE
            + self.seconds
            + Decimal(self.miliseconds * calendar.SECONDS_IN_MILI)
            + Decimal(self.microseconds * calendar.SECONDS_IN_MICRO)
            + Decimal(self.nanoseconds * calendar.SECONDS_IN_NANO)
        )
        return days_seconds

    @staticmethod
    def _is_character_valid(duration) -> None:
        duration_symbols = ["P", "T", "Y", "M", "D", "H", "M", "S", "m", "u", "n"]
        for ch in duration:
            if ch.isalpha() and ch not in duration_symbols:
                raise IncorrectDesignator(designator=ch)

    @staticmethod
    def _validate_pattern(duration) -> None:
        if not ISO8601_PERIOD_REGEX.match(duration):
            raise IncorrectPattern()

    @staticmethod
    def _is_validate_number(duration_dict: dict) -> None:
        for key, value in duration_dict.items():
            if isinstance(value, int) and value >= 0:
                continue
            raise IncorrectNumber()

    def _parse_time_duration(self, duration: str) -> dict:
        time_value = re.findall(r"T.*", duration)
        if time_value:
            match = re.findall(
                r"\d*H|\d*M|\d*S|\d*m|\d*u|\d*n",
                time_value[0],
            )
            if match:
                duration_dict = convert_to_dict(match, add_letter="t")
                self._is_validate_number(duration_dict)
                return duration_dict
        return {}

    def _parse_date_duration(self, duration) -> dict:
        date_value = re.match(r"^P:?(\S*)T", duration)
        if date_value:
            match = re.findall(r"\d*Y|\d*M|\d*D", date_value[0])
            if match:
                duration_dict = convert_to_dict(match, add_letter="p")
                self._is_validate_number(duration_dict)
                return duration_dict
        return {}

    def parse(self, duration: str) -> ISODuration:
        self._is_character_valid(duration)
        self._validate_pattern(duration)
        duration_dict = self._parse_date_duration(duration)
        duration_dict.update(self._parse_time_duration(duration))
        return self._wrap(duration_dict)

    def _generate_date(self, duration_dict: dict) -> str:
        date_duration = rename(duration_dict, self.date_map_dict)
        date_string = ""
        for key, value in date_duration.items():
            if value != 0:
                date_string = date_string + str(value) + str(key)
        return "P" + date_string

    def _generate_time(self, duration_dict: dict) -> str:
        time_duration = rename(duration_dict, self.time_map_dict)
        time_string = ""
        for key, value in time_duration.items():
            if value != 0:
                time_string = time_string + str(value) + str(key)
        return "T" + time_string

    def _remove_date(self, duration_dict: dict) -> dict:
        for key, value in self.date_map_dict.items():
            del duration_dict[key]
        return duration_dict

    def generate(self, duration: ISODuration) -> str:
        duration_dict = duration.__dict__
        self._is_validate_number(duration_dict)
        gen_date = self._generate_date(duration_dict)
        duration_dict = self._remove_date(duration_dict)
        gen_time = self._generate_time(duration_dict)

        return gen_date + gen_time

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, ISODuration):
            return self.get_seconds() == other.get_seconds()

    def __gt__(self, other: "ISODuration"):
        if isinstance(other, ISODuration):
            return self.get_seconds() > other.get_seconds()

    def __lt__(self, other: "ISODuration"):
        if isinstance(other, ISODuration):
            return self.get_seconds() < other.get_seconds()

    def __ge__(self, other: "ISODuration"):
        if isinstance(other, ISODuration):
            return self.get_seconds() >= other.get_seconds()

    def __le__(self, other: "ISODuration"):
        if isinstance(other, ISODuration):
            return self.get_seconds() <= other.get_seconds()
