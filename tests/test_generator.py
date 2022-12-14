from _pytest.python_api import raises

from src.duration import iso_duration
from src.duration.duration import Duration
from src.duration.exceptions import IncorrectPattern, IncorrectValue


def test_generator():
    expected_result = "P3Y6M4DT12H24M12S10m80u12n"
    duration_dict = {
        "years": 3,
        "months": 6,
        "days": 4,
        "hours": 12,
        "minutes": 24,
        "seconds": 12,
        "miliseconds": 10,
        "microseconds": 80,
        "nanoseconds": 12,
    }
    duration = Duration(duration_dict)
    generated_duration = iso_duration.generate(duration)
    assert generated_duration == expected_result


def test_invalid_float_number():
    with raises(IncorrectValue):
        duration_dict = {"years": 3.1}
        duration = Duration(duration_dict)
        iso_duration.generate(duration)


def test_invalid_negative_number():
    with raises(IncorrectValue):
        duration_dict = {"years": -3}
        duration = Duration(duration_dict)
        iso_duration.generate(duration)
