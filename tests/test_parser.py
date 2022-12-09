from _pytest.python_api import raises

from src.duration_parser.exceptions import IncorrectDesignator
from src.duration_parser.iso_duration import ISODuration


def test_parser():
    s = "P3Y6M4DT12H24M12S10m12n80u"
    s2 = "PT1n"
    s3 = "P1DT"
    s4 = "P3Y6M4DT12H24M12S10m12n80u"
    s5 = "P3Y6M4DT12H24M12S10m12n90u"

    duration_list = [s, s2, s3, s4, s5]
    for duration_value in duration_list:
        d = ISODuration().parse(duration_value)
        assert ISODuration().generate(d) == duration_value


def test_incorrect_designator():
    duration_string = "x3Y6M4DT12H24M12S10m12n80u"
    with raises(IncorrectDesignator):
        ISODuration().parse(duration_string)


def test_valid_parser():
    year = 3
    month = 6
    day = 4
    hour = 12
    minute = 24
    seconds = 12
    miliseconds = 10
    microseconds = 80
    nanoseconds = 12
    duration_string = "P3Y6M4DT12H24M12S10m12n80u"
    iso_duration = ISODuration().parse(duration_string)
    assert iso_duration.years == year
    assert iso_duration.months == month
    assert iso_duration.days == day
    assert iso_duration.hours == hour
    assert iso_duration.minutes == minute
    assert iso_duration.seconds == seconds
    assert iso_duration.miliseconds == miliseconds
    assert iso_duration.microseconds == microseconds
    assert iso_duration.nanoseconds == nanoseconds
