from src.duration_parser import iso_duration


def test_parser():
    s = "P3Y6M4DT12H24M12S10m80u12n"
    s2 = "PT1n"
    s3 = "P1DT"
    s4 = "P3Y6M4DT12H24M12S10m80u12n"
    s5 = "P3Y6M4DT12H24M12S10m90u12n"

    duration_list = [s, s2, s3, s4, s5]
    for duration_value in duration_list:
        d = iso_duration.parse(duration_value)
        assert iso_duration.generate(d) == duration_value


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
    s1 = "P1DT"
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
