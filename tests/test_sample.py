from os import environ, getenv

import pytest

from CHANGE_ME.module1 import hello


def test_module1():
    assert hello() == "Hello world"
    assert hello() != "I should fail"


def test_raising_errors():
    def f():
        raise SystemExit(1)

    with pytest.raises(SystemExit):
        f()


def test_foo(mocker):
    assert getenv("testVar") is None
    mocker.patch.dict(environ, {"testVar": "test_value"})
    assert getenv("testVar") == "test_value"
