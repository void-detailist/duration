from decimal import Decimal


class DeltaDuration:
    def __init__(
        self,
        to_years: int,
        to_seconds: Decimal,
        to_months: int,
        to_days: int,
        to_hours: int,
        to_minutes: int,
        to_miliseconds: Decimal,
        to_microseconds: Decimal,
        to_nanoseconds: Decimal,
    ):
        self.to_years = to_years
        self.to_seconds = to_seconds
        self.to_months = to_months
        self.to_days = to_days
        self.to_hours = to_hours
        self.to_minutes = to_minutes
        self.to_miliseconds = to_miliseconds
        self.to_microseconds = to_microseconds
        self.to_nanoseconds = to_nanoseconds

    def __eq__(self, other):
        if isinstance(other, DeltaDuration):
            return self.to_seconds == other.to_seconds
        else:
            return self.to_seconds == other

    def __repr__(self):
        return str(self.__dict__)

    def __gt__(self, other):
        if isinstance(other, DeltaDuration):
            return self.to_seconds > other.to_seconds
        else:
            return self.to_seconds > other

    def __lt__(self, other):
        if isinstance(other, DeltaDuration):
            return self.to_seconds < other.to_seconds
        return self.to_seconds < other

    def __ge__(self, other):
        if isinstance(other, DeltaDuration):
            return self.to_seconds >= other.to_seconds
        return self.to_seconds >= other

    def __le__(self, other):
        if isinstance(other, DeltaDuration):
            return self.to_seconds <= other.to_seconds
        return self.to_seconds
