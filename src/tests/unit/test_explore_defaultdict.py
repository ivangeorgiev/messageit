from typing import DefaultDict

import pytest

class TestDefaultDict:
    @pytest.fixture(name="some_dict")
    def given_some_dict(self):
        return DefaultDict(int)

    @pytest.fixture(name="some_key")
    def given_some_key(self):
        return "a"

    @pytest.fixture(name="when_key_is_accessed")
    def when_key_is_accessed(self, some_dict, some_key):
        return some_dict[some_key]

    def check_key_in_dict(self, dict_, key_):
        return key_ in dict_

    @pytest.fixture
    def when_check_key_in_dict(self, some_dict, some_key):
        return some_key in some_dict

    def test_accessing_a_key_creates_it(
        self, some_dict, some_key, when_key_is_accessed
    ):
        assert len(some_dict.keys()) == 1
        assert some_key in some_dict
        assert when_key_is_accessed == 0

    def test_checking_for_a_key_doesnt_create_it(
        self, some_dict, some_key, request
    ):
        check_result = request.getfixturevalue("when_check_key_in_dict")
        assert not check_result
        assert len(some_dict.keys()) == 0
