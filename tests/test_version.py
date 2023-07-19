from datetime import date, datetime

import pytest
from beanie import PydanticObjectId

from src.domain.version import Version


@pytest.mark.parametrize("datetime_format, expected_result", [
    # Valid date formats
    (date(2023, 7, 4), datetime(2023, 7, 4)),
    ('2023-07-01', datetime(2023, 7, 1)),
    ('2023-07-02 01:02:03', datetime(2023, 7, 2, 1, 2, 3)),
    ('2023-07-03T01:02:03', datetime(2023, 7, 3, 1, 2, 3)),
    # Invalid date formats
    (20230719, None),
    ("2023-07-32", None),
    (["2023", "07", "19"], None),
    ({"datetime": "2023-07-19"}, None),
])
def test_version_validate_datetime_formats(datetime_format, expected_result):
    if expected_result:
        result = Version.validate_datetime(datetime_format)
        assert result == expected_result
    else:
        with pytest.raises(ValueError, match="Invalid format"):
            Version.validate_datetime(datetime_format)


@pytest.mark.parametrize("author_id, expected_author_id", [
    (PydanticObjectId("64b6c604ecc8c97d5694bcc8"), PydanticObjectId("64b6c604ecc8c97d5694bcc8"))
])
def test_version_new_with_author_id(author_id, expected_author_id):
    version = Version()
    version.new(author_id=author_id)
    assert version.author_id == expected_author_id


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


def test_version_new_default_values_for_approved_deleted():
    version = Version()
    author_id = PydanticObjectId()
    version.new(author_id)
    assert version.approved is False
    assert version.deleted is False


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
