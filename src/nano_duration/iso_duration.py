from __future__ import annotations

import re

from nano_duration import calendar
from nano_duration.delta_duration import DeltaDuration
from nano_duration.duration import Duration
from nano_duration.exceptions import IncorrectPattern

ISO8601_PERIOD_REGEX = re.compile(
    r"P(?!\b)"
    r"(?P<years>\d(\d+)?Y)?"
    r"(?P<months>\d(\d+)?M)?"
    r"(?P<days>\d(\d+)?D)?"
    r"((?P<separator>T)(?P<hours>\d+(\d+)?H)?"
    r"(?P<minutes>\d(\d+)?M)?"
    r"(?P<seconds>\d(\d+)?S)?"
    r"(?P<miliseconds>\d(\d+)?m)?"
    r"(?P<microseconds>\d+(\d+)?u)?"
    r"(?P<nanoseconds>\d+(\d+)?n)?)?$"
)


def generate(duration: Duration) -> str:
    duration_dict = duration.__dict__
    _ = (
        lambda key, symbol: f"{duration_dict[key]}{symbol}"
        if duration_dict.get(key, 0) > 0
        else ""
    )
    _date = "P" + "".join([_("years", "Y"), _("months", "M"), _("days", "D")])

    _time = "".join(
        [
            _("hours", "H"),
            _("minutes", "M"),
            _("seconds", "S"),
            _("miliseconds", "m"),
            _("microseconds", "u"),
            _("nanoseconds", "n"),
        ]
    )
    if _time:
        _time = "T" + _time
    return f"{_date}{_time}"


def parse(duration: str) -> Duration:
    match = ISO8601_PERIOD_REGEX.match(duration)
    if duration[-1] == "T":
        raise IncorrectPattern()
    if match:
        group = match.groupdict()
        duration_dict = {
            "years": split(group.get("years")),
            "months": split(group.get("months")),
            "days": split(group.get("days")),
            "hours": split(group.get("hours")),
            "minutes": split(group.get("minutes")),
            "seconds": split(group.get("seconds")),
            "miliseconds": split(group.get("miliseconds")),
            "microseconds": split(group.get("microseconds")),
            "nanoseconds": split(group.get("nanoseconds")),
        }
    else:
        raise IncorrectPattern()
    return Duration(**duration_dict)


def split(string_value) -> int:
    if string_value is not None:
        return int(string_value[:-1])
    return 0


def calculate_duration_parts(duration: Duration) -> DeltaDuration:
    seconds = float(duration.get_seconds())
    years = seconds // calendar.SECONDS_IN_YEAR
    months = seconds // calendar.SECONDS_IN_MONTH
    days = seconds // calendar.SECONDS_IN_DAY
    hours = seconds // calendar.SECONDS_IN_HOUR
    minutes = seconds // calendar.SECONDS_IN_MINUTE
    miliseconds = seconds // calendar.SECONDS_IN_MILI
    microseconds = seconds // calendar.SECONDS_IN_MICRO
    nanoseconds = seconds // calendar.SECONDS_IN_NANO
    return DeltaDuration(
        to_years=years,
        to_seconds=seconds,
        to_months=months,
        to_days=days,
        to_hours=hours,
        to_minutes=minutes,
        to_miliseconds=miliseconds,
        to_microseconds=microseconds,
        to_nanoseconds=nanoseconds,
    )
