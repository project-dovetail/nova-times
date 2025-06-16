import pytest

from nova_times.exceptions import MissingDataError


def test_missing_data_error():
    with pytest.raises(MissingDataError) as err:
        raise MissingDataError("a message")
    assert str(err.value) == "a message"
