from src.nano_duration.delta_duration import DeltaDuration
from src.nano_duration.duration import Duration
from src.nano_duration.iso_duration import calculate_duration_parts


def test_calculate_duration_parts():
    # Test duration of 2 years and 365 days
    duration = Duration(years=2, days=365)
    delta_duration = {
        "to_years": 3.0,
        "to_months": 35.0,
        "to_days": 1077.0,
        "to_hours": 25848.0,
        "to_minutes": 1550880.0,
        "to_seconds": 93052800.0,
        "to_miliseconds": 93052799999.0,
        "to_microseconds": 93052800000000.0,
        "to_nanoseconds": 9.30528e16,
    }
    expected_duration_parts = DeltaDuration(**delta_duration)
    assert calculate_duration_parts(duration) == expected_duration_parts
