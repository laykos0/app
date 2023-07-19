from datetime import date, datetime

import pytest
from beanie import PydanticObjectId

from src.domain.version import Version


@pytest.mark.parametrize("datetime_format, expected_result", [
    (date(2023, 7, 4), datetime(2023, 7, 4)),
    ('2023-07-01', datetime(2023, 7, 1)),
    ('2023-07-02 01:02:03', datetime(2023, 7, 2, 1, 2, 3)),
    ('2023-07-03T01:02:03', datetime(2023, 7, 3, 1, 2, 3)),
])
def test_version_validate_datetime_valid_formats(datetime_format, expected_result):
    result = Version.validate_datetime(datetime_format)
    assert result == expected_result


@pytest.mark.parametrize("datetime_format", [
    20230719,
    "2023-07-32",
    ["2023", "07", "19"],
    {"datetime": "2023-07-19"},
])
def test_version_validate_datetime_invalid_formats(datetime_format):
    with pytest.raises(ValueError, match="Invalid format"):
        Version.validate_datetime(datetime_format)


def test_version_new_default_values():
    version = Version()
    number = version.number
    author_id = PydanticObjectId()
    version.new(author_id)
    assert version.approved is False
    assert version.deleted is False
    assert version.number == number + 1


@pytest.mark.parametrize("number, expected_number", [
    (0, 1),
    (5, 6),
    (2 ** 31, 2 ** 31 + 1),
])
def test_version_new_number_increment(number, expected_number):
    version = Version()
    version.number = number
    version.new(PydanticObjectId())
    assert version.number == expected_number


@pytest.mark.parametrize("approved, deleted", [
    (True, True),
    (True, False),
    (False, True),
    (False, False),
])
def test_version_new_with_approved_deleted(approved, deleted):
    version = Version()
    version.new(PydanticObjectId(), approved=approved, deleted=deleted)
    assert version.approved == approved
    assert version.deleted == deleted


@pytest.mark.parametrize("author_id, expected_author_id", [
    (PydanticObjectId("64b6c604ecc8c97d5694bcc8"), PydanticObjectId("64b6c604ecc8c97d5694bcc8"))
])
def test_version_new_with_author_id(author_id, expected_author_id):
    version = Version()
    version.new(author_id=author_id)
    assert version.author_id == expected_author_id
