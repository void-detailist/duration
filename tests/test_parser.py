from decimal import Decimal

from src.nano_duration import iso_duration


def test_parser():
    duration_string_one = "P3Y6M4DT12H24M12S10m"
    expected_result_one = Decimal("108217452.0100000000000000002")

    duration_string_two = "P1D"
    expected_result_two = 86400

    duration_string_three = "P3Y"
    expected_result_three = 92275200

    durations = [duration_string_one, duration_string_two, duration_string_three]
    expected_results = [expected_result_one, expected_result_two, expected_result_three]
    for duration_value, result in zip(durations, expected_results):
        duration = iso_duration.parse(duration_value)
        assert duration.get_seconds() == result


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
    duration_string = "P3Y6M4DT12H24M12S10m80u12n"
    duration = iso_duration.parse(duration_string)
    assert duration.years == year
    assert duration.months == month
    assert duration.days == day
    assert duration.hours == hour
    assert duration.minutes == minute
    assert duration.seconds == seconds
    assert duration.miliseconds == miliseconds
    assert duration.microseconds == microseconds
    assert duration.nanoseconds == nanoseconds


def test_comparison():
    s1 = "P1D"
    s2 = "PT1n"
    duration_1 = iso_duration.parse(s1)
    duration_2 = iso_duration.parse(s2)
    assert duration_1 > duration_2
    s1 = "P3Y6M4DT12H24M12S10m80u12n"
    s2 = "P3Y6M4DT12H24M12S10m80u12n"
    duration_1 = iso_duration.parse(s1)
    duration_2 = iso_duration.parse(s2)
    assert duration_1 == duration_2

    s1 = "P3Y6M4DT12H24M12S10m90u12n"
    s2 = "P3Y6M4DT12H24M12S10m80u12n"
    duration_1 = iso_duration.parse(s1)
    duration_2 = iso_duration.parse(s2)
    assert duration_2 < duration_1

    seconds_value = 12
    assert duration_2 > seconds_value
