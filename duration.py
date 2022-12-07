import pickle
from datetime import date


class custom_date(date):
    def __new__(cls, year, month, day):
        return date.__new__(cls, year, month, day)


class Duration(object):
    def __init__(self, dikt: dict):
        self.Year: int = dikt.get("pY") or 0
        self.Month: int = dikt.get("pM") or 0
        self.Day: int = dikt.get("pD") or 0
        self.Hour: int = dikt.get("tH") or 0
        self.Minute: int = dikt.get("tM") or 0
        self.seconds: int = dikt.get("tS") or 0
        self.miliseconds: int = dikt.get("tm") or 0
        self.nanoseconds: int = dikt.get("tn") or 0
        self.microseconds: int = dikt.get("tu") or 0

    def __str__(self):
        return (
            f"{self.Year}year {self.Month}month {self.Day}day {self.Hour}hour {self.Minute}minute {self.seconds}seconds"
            f" {self.miliseconds}miliseconds {self.nanoseconds}nanoseconds {self.microseconds}microseconds"
        )

    def __eq__(self, other):
        return pickle.dumps(self) == pickle.dumps(other)

    def __gt__(self, other):
        pass
