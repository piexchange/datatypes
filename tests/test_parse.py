
import pytest

from datatypes import *


@pytest.mark.parametrize('value_to_parse, cls, expected_result', [
    ('1,2,3', List, ['1', '2', '3']),
    ('1,2,3', List[int], [1, 2, 3]),
    ('1.5=3 0=5', Dict[float, int], {1.5: 3, 0: 5}),
    ('true', Boolean, True),
    ('False', Boolean, False),
])
def test_parse(value_to_parse, cls, expected_result):
    result = cls.parse(value_to_parse)
    assert result == expected_result
