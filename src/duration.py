from decimal import Decimal

from calendar import CALENDAR


class Duration(object):
    def __init__(self, dikt: dict):
        self.years: int = dikt.get("pY") or 0
        self.months: int = dikt.get("pM") or 0
        self.days: int = dikt.get("pD") or 0
        self.hours: int = dikt.get("tH") or 0
        self.minutes: int = dikt.get("tM") or 0
        self.seconds: int = dikt.get("tS") or 0
        self.miliseconds: int = dikt.get("tm") or 0
        self.nanoseconds: int = dikt.get("tn") or 0
        self.microseconds: int = dikt.get("tu") or 0

    def get_seconds(self):
        days_seconds = (
            self.years * CALENDAR.SECONDS_IN_YEAR
            + self.months * CALENDAR.SECONDS_IN_MONTH
            + self.days * CALENDAR.SECONDS_IN_DAY
            + self.hours * CALENDAR.SECONDS_IN_HOUR
            + self.minutes * CALENDAR.SECONDS_IN_MINUTE
            + self.seconds
            + self.miliseconds * CALENDAR.SECONDS_IN_MILI
            + self.microseconds * CALENDAR.SECONDS_IN_MICRO
            + self.nanoseconds * CALENDAR.SECONDS_IN_NANO
        )
        return Decimal(days_seconds)

    def __str__(self):
        return (
            f"{self.years}year {self.months}month {self.days}day {self.hours}hour {self.minutes}minute {self.seconds}seconds"
            f" {self.miliseconds}miliseconds {self.microseconds}microseconds  {self.nanoseconds}nanoseconds"
        )

    def __eq__(self, other):
        if isinstance(other, Duration):
            return self.get_seconds() == other.get_seconds()

    def __gt__(self, other: "Duration"):
        if isinstance(other, Duration):
            return self.get_seconds() > other.get_seconds()

    def __lt__(self, other):
        if isinstance(other, Duration):
            return self.get_seconds() < other.get_seconds()

    def __ge__(self, other):
        if isinstance(other, Duration):
            return self.get_seconds() >= other.get_seconds()

    def __le__(self, other):
        if isinstance(other, Duration):
            return self.get_seconds() <= other.get_seconds()
