from fntypes.result import Result, Ok, Error
from fntypes.error import UnwrapError
from fntypes.option import Nothing, Some
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
    assert result.map_or(10, lambda v: v + v) == Ok(2)
    assert result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == Ok(1)
    assert result.and_then(inc_number).unwrap() == 2
    assert repr(result) == "<Result: Ok(1)>"
    assert result.expect("Should not happen") == 1
    assert isinstance(result.cast(Some, Nothing), Some)
    assert result.cast(Some, Nothing).unwrap() == 1

    assert result.cast() == result

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
    assert result.map_or(5, lambda _: 6) == Ok(5)
    assert result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == Ok(2)
    assert result.and_then(inc_number).error.args[0] == "Oh"
    assert repr(result) == "<Result: Error(TypeError: 'Oh')>"

    with pytest.raises(UnwrapError) as exc_info:
        assert result.expect(ValueError())
    
    assert isinstance(exc_info._excinfo[1].args[0], ValueError)  # type: ignore

    with pytest.raises(UnwrapError):
        result.cast(Some, Nothing).unwrap()

    assert result.cast() == result
    
    x = result.cast(Some, Nothing)
    assert isinstance(x, Nothing)
    assert x.error is None
    
def test_nothing():
    nothing = Nothing()
    with pytest.raises(UnwrapError, match='None'):
        nothing.unwrap()
    
    assert repr(nothing) == "Nothing()"
    assert nothing.map(lambda _: object()) == nothing
    assert nothing.and_then(lambda x: Some(123)) == nothing

def test_some():
    option = Some(1)
    assert repr(option) == "Some(1)"
    assert option.map(lambda x: x + 1) == Some(2)
    assert option.and_then(lambda x: Nothing()) == Nothing()


def test_log_factory():
    dct = {}
    RESULT_ERROR_LOGGER.set_log(lambda err: dct.update({"err": err}))
    RESULT_ERROR_LOGGER.set_traceback_formatter(lambda: "")

    Error("Error msg")
    
    assert dct["err"].endswith(repr("Error msg"))
