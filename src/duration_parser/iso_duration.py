from __future__ import annotations

import re
from decimal import Decimal

from . import calendar
from .exceptions import IncorrectDesignator, IncorrectNumber, IncorrectPattern
from .util import convert_to_dict, rename


class ISODuration(object):
    date_map_dict = {"years": "Y", "months": "M", "days": "D"}

    time_map_dict = {
        "hours": "H",
        "minutes": "M",
        "seconds": "S",
        "miliseconds": "m",
        "nanoseconds": "n",
        "microseconds": "u",
    }

    def __init__(self):
        self.years: int = 0
        self.months: int = 0
        self.days: int = 0
        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0
        self.miliseconds: int = 0
        self.nanoseconds: int = 0
        self.microseconds: int = 0

    def _wrap(self, duration_dict: dict) -> ISODuration:
        self.years = duration_dict.get("pY") or 0
        self.months = duration_dict.get("pM") or 0
        self.days = duration_dict.get("pD") or 0
        self.hours = duration_dict.get("tH") or 0
        self.minutes = duration_dict.get("tM") or 0
        self.seconds = duration_dict.get("tS") or 0
        self.miliseconds = duration_dict.get("tm") or 0
        self.nanoseconds = duration_dict.get("tn") or 0
        self.microseconds = duration_dict.get("tu") or 0
        return self

    def get_seconds(self) -> Decimal:
        days_seconds = (
            self.years * calendar.SECONDS_IN_YEAR
            + self.months * calendar.SECONDS_IN_MONTH
            + self.days * calendar.SECONDS_IN_DAY
            + self.hours * calendar.SECONDS_IN_HOUR
            + self.minutes * calendar.SECONDS_IN_MINUTE
            + self.seconds
            + self.miliseconds * calendar.SECONDS_IN_MILI
            + self.microseconds * calendar.SECONDS_IN_MICRO
            + self.nanoseconds * calendar.SECONDS_IN_NANO
        )
        return Decimal(days_seconds)

    def _is_character_valid(self, duration) -> None:
        duration_symbols = ["P", "T", "Y", "M", "D", "H", "M", "S", "m", "u", "n"]
        for ch in duration:
            if ch.isalpha() and ch not in duration_symbols:
                raise IncorrectDesignator(designator=ch)

    def _is_pattern_valid(self, duration) -> None:
        if not re.match(r"^P:?(\S*)T", duration):
            raise IncorrectPattern()

    def _is_number_valid(self, duration_dict: dict) -> None:
        for key, value in duration_dict.items():
            if isinstance(value, int) and value >= 0:
                continue
            raise IncorrectNumber()

    def _parse_time_duration(self, duration: str) -> dict:
        self._is_character_valid(duration)
        self._is_pattern_valid(duration)
        time_value = re.findall(r"T.*", duration)
        if time_value:
            match = re.findall(
                r"\d*H|\d*M|\d*S|\d*m|\d*u|\d*n",
                time_value[0],
            )
            if match:
                duration_dict = convert_to_dict(match, add_letter="t")
                self._is_number_valid(duration_dict)
                return duration_dict
        return {}

    def _parse_date_duration(self, duration) -> dict:
        self._is_character_valid(duration)
        self._is_pattern_valid(duration)
        date_value = re.match(r"^P:?(\S*)T", duration)
        if date_value:
            match = re.findall(r"\d*Y|\d*M|\d*D", date_value[0])
            if match:
                duration_dict = convert_to_dict(match, add_letter="p")
                self._is_number_valid(duration_dict)
                return duration_dict
        return {}

    def parse(self, duration: str) -> ISODuration:
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
        self._is_number_valid(duration_dict)
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
