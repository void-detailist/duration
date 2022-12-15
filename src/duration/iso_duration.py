from __future__ import annotations

import re

from .duration import Duration
from .exceptions import IncorrectPattern

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
    _time = "T" + "".join(
        [
            _("hours", "H"),
            _("minutes", "M"),
            _("seconds", "S"),
            _("miliseconds", "m"),
            _("microseconds", "u"),
            _("nanoseconds", "n"),
        ]
    )
    return f"{_date}{_time}"


def parse(duration: str) -> Duration:
    match = ISO8601_PERIOD_REGEX.match(duration)
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
    return Duration(duration_dict)


def split(string_value) -> int:
    if string_value is not None:
        return int(string_value[:-1])
    return 0
