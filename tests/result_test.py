from monading.result import Result, Ok, Error
import pytest


def test_result_ok():
    result = Ok(1)
    assert result.unwrap() == 1
    assert result.unwrap_or(2) == 1
    assert result.unwrap_or_else(lambda err: 2) == 1
    assert result.unwrap_or_other(Error(None)) == 1

    assert result.map(lambda v: 22 / v) == Ok(22)
    assert result.map_or(10, lambda v: v + v) == 2
    assert result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == 1

def test_result_err():
    result: Result[int, TypeError] = Error(TypeError("Oh"))
    with pytest.raises(TypeError):
        assert result.unwrap()

    assert result.unwrap_or(1) == 1
    assert result.unwrap_or_else(lambda err: err.args[0]) == "Oh"
    assert result.unwrap_or_other(Ok(10)) == 10
    assert result.map(lambda _: 2) == result
    assert result.map_or(5, lambda _: 6) == 5
    assert result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == 2

    with pytest.raises(ValueError):
        assert result.expect(ValueError)


