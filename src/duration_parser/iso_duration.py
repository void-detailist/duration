from __future__ import annotations

import re

from . import util
from .duration import Duration
from .exceptions import IncorrectDesignator, IncorrectNumber, IncorrectPattern

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
date_map_dict = {"years": "Y", "months": "M", "days": "D"}

time_map_dict = {
    "hours": "H",
    "minutes": "M",
    "seconds": "S",
    "miliseconds": "m",
    "microseconds": "u",
    "nanoseconds": "n",
}


def generate(duration: Duration) -> str:
    duration_dict = duration.__dict__
    _validate_number(duration_dict)
    gen_date = _generate_date(duration_dict)
    duration_dict = _remove_date(duration_dict)
    gen_time = _generate_time(duration_dict)
    return gen_date + gen_time


def parse(duration: str) -> Duration:
    _is_character_valid(duration)
    _validate_pattern(duration)
    duration_dict = _parse_date_duration(duration)
    duration_dict.update(_parse_time_duration(duration))
    return Duration(duration_dict)


def _is_character_valid(duration) -> None:
    duration_symbols = ["P", "T", "Y", "M", "D", "H", "M", "S", "m", "u", "n"]
    for ch in duration:
        if ch.isalpha() and ch not in duration_symbols:
            raise IncorrectDesignator(designator=ch)


def _validate_pattern(duration) -> None:
    if not ISO8601_PERIOD_REGEX.match(duration):
        raise IncorrectPattern()


def _validate_number(duration_dict: dict) -> None:
    for key, value in duration_dict.items():
        if isinstance(value, int) and value >= 0:
            continue
        raise IncorrectNumber()


def _parse_time_duration(duration: str) -> dict:
    time_value = re.findall(r"T.*", duration)
    if time_value:
        match = re.findall(
            r"\d*H|\d*M|\d*S|\d*m|\d*u|\d*n",
            time_value[0],
        )
        if match:
            duration_dict = util.convert_to_dict(match)
            duration_dict = util.rename_dict(
                duration_dict, util.switch_key_value(time_map_dict)
            )
            return duration_dict
    return {}


def _parse_date_duration(duration) -> dict:
    date_value = re.match(r"^P:?(\S*)T", duration)
    if date_value:
        match = re.findall(r"\d*Y|\d*M|\d*D", date_value[0])
        if match:
            duration_dict = util.convert_to_dict(match)
            _validate_number(duration_dict)
            duration_dict = util.rename_dict(
                duration_dict, util.switch_key_value(date_map_dict)
            )
            return duration_dict
    return {}


def _generate_date(duration_dict: dict) -> str:
    date_duration = util.rename_dict(duration_dict, date_map_dict)
    date_string = ""
    for key, value in date_duration.items():
        if value != 0:
            date_string = date_string + str(value) + str(key)
    return "P" + date_string


def _generate_time(duration_dict: dict) -> str:
    time_duration = util.rename_dict(duration_dict, time_map_dict)
    time_string = ""
    for key, value in time_duration.items():
        if value != 0:
            time_string = time_string + str(value) + str(key)
    return "T" + time_string


def _remove_date(duration_dict: dict) -> dict:
    for key, value in date_map_dict.items():
        del duration_dict[key]
    return duration_dict
