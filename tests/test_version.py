from datetime import datetime
from src.domain.version import Version


def test_validate_datetime_format_one():
    iso_string = '2023-07-01'
    expected_result = datetime(2023, 7, 1)
    result = Version.validate_datetime(iso_string)
    assert result == expected_result


def test_validate_datetime_format_two():
    iso_string = '2023-07-02 01:02:03'
    expected_result = datetime(2023, 7, 2, 1, 2, 3)
    result = Version.validate_datetime(iso_string)
    assert result == expected_result


def test_validate_datetime_format_three():
    iso_string = '2023-07-03T01:02:03'
    expected_result = datetime(2023, 7, 3, 1, 2, 3)
    result = Version.validate_datetime(iso_string)
    assert result == expected_result

