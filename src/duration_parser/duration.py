from decimal import Decimal

from . import calendar


class Duration(object):
    def __init__(self, duration_dict: dict):
        self.years = duration_dict.get("years", 0)
        self.months = duration_dict.get("months", 0)
        self.days = duration_dict.get("days", 0)
        self.hours = duration_dict.get("hours", 0)
        self.minutes = duration_dict.get("minutes", 0)
        self.seconds = duration_dict.get("seconds", 0)
        self.miliseconds = duration_dict.get("miliseconds", 0)
        self.microseconds = duration_dict.get("microseconds", 0)
        self.nanoseconds = duration_dict.get("nanoseconds", 0)

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

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, Duration):
            return self.get_seconds() == other.get_seconds()

    def __gt__(self, other: "Duration"):
        if isinstance(other, Duration):
            return self.get_seconds() > other.get_seconds()

    def __lt__(self, other: "Duration"):
        if isinstance(other, Duration):
            return self.get_seconds() < other.get_seconds()

    def __ge__(self, other: "Duration"):
        if isinstance(other, Duration):
            return self.get_seconds() >= other.get_seconds()

    def __le__(self, other: "Duration"):
        if isinstance(other, Duration):
            return self.get_seconds() <= other.get_seconds()
