from _pytest.python_api import raises

from src.duration_parser.exceptions import IncorrectNumber
from src.duration_parser.iso_duration import ISODuration


def test_generator():
    expected_result = "P3Y6M4DT12H24M12S10m12n80u"
    duration = ISODuration()
    duration.years = 3
    duration.months = 6
    duration.days = 4
    duration.hours = 12
    duration.minutes = 24
    duration.seconds = 12
    duration.miliseconds = 10
    duration.nanoseconds = 12
    duration.microseconds = 80
    generated_duration = ISODuration().generate(duration)
    assert generated_duration == expected_result


def test_invalid_float_number():
    with raises(IncorrectNumber):
        duration = ISODuration()
        duration.years = 3.1
        ISODuration().generate(duration)


def test_invalid_negative_number():
    with raises(IncorrectNumber):
        duration = ISODuration()
        duration.years = -2
        ISODuration().generate(duration)
