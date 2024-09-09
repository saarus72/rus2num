import json

import pytest

from rus2num import Rus2Num

r2n = Rus2Num()


with open("tests/gt.json") as f:

    @pytest.mark.parametrize("input, expected", json.load(f).items())
    def test_replace(input, expected):
        assert r2n(input) == expected
