from datetime import datetime

import pytest

from src.domain.version import Version


@pytest.mark.parametrize("datetime_format, expected_result", [('2023-07-01', datetime(2023, 7, 1)),
                                                              ('2023-07-02 01:02:03', datetime(2023, 7, 2, 1, 2, 3)),
                                                              ('2023-07-03T01:02:03', datetime(2023, 7, 3, 1, 2, 3))])
def test_validate_datetime_format(datetime_format, expected_result):
    result = Version.validate_datetime(datetime_format)
    assert result == expected_result
