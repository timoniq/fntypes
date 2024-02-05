from fntypes.result import Result, Ok, Error
from fntypes.error import UnwrapError
from fntypes.option import Nothing
from fntypes.result.log_factory import RESULT_ERROR_LOGGER
import pytest


def inc_number(n: int) -> Result[int, TypeError]:
    return Ok(n + 1)


def test_result_ok():

    result = Ok(1)
    assert result.unwrap() == 1
    assert result
    assert result != Error("Oh")  # type: ignore
    assert result.unwrap_or(2) == 1
    assert result.unwrap_or_none() == 1
    assert result.unwrap_or_other(Error(None)) == 1

    assert result.map(lambda v: 22 / v) == Ok(22)
    assert result.map_or(10, lambda v: v + v) == 2
    assert result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == 1
    assert result.and_then(inc_number).unwrap() == 2
    assert repr(result) == "<Result: Ok(1)>"
    assert result.expect("Should not happen") == 1

def test_result_err():
    result: Result[int, TypeError] = Error(TypeError("Oh"))
    with pytest.raises(TypeError):
        assert result.unwrap()

    assert result.unwrap_or(1) == 1
    assert not result
    assert result != Ok(1)
    assert result.unwrap_or_none() is None
    assert result.unwrap_or_other(Ok(10)) == 10
    assert result.map(lambda _: 2) == result
    assert result.map_or(5, lambda _: 6) == 5
    assert result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == 2
    assert result.and_then(inc_number).error.args[0] == "Oh"
    assert repr(result) == "<Result: Error(TypeError: 'Oh')>"

    with pytest.raises(ValueError):
        assert result.expect(ValueError)

def test_nothing():
    nothing = Nothing()
    with pytest.raises(UnwrapError, match='None'):
        nothing.unwrap()
    

def test_log_factory():
    dct = {}
    RESULT_ERROR_LOGGER.set_log(lambda err: dct.update({"err": err}))
    RESULT_ERROR_LOGGER.set_traceback_formatter(lambda: "")

    Error("Error msg")
    
    assert dct["err"].endswith(repr("Error msg"))
