import pytest

from fntypes.library.error.error import UnwrapError
from fntypes.library.monad.option import Nothing


def test_unwrap_error_with_error_with_attributes() -> None:
    class TestError(Exception):
        def __init__(self, message: str, value: object | None = None) -> None:
            self.message = message
            self.value = value

    try:
        raise UnwrapError(TestError("Hello", 123))
    except TestError as e:
        assert e.message == "Hello"
        assert e.value == 123


def test_nested_unwrap_errors_with_error_with_attributes() -> None:
    class TestError(Exception):
        def __init__(self, message: str, value: object | None = None) -> None:
            self.message = message
            self.value = value

    try:
        raise UnwrapError(UnwrapError(TestError("World", value=[])))
    except TestError as e:
        assert e.message == "World"
        assert e.value == []


def test_unwrap_error_with_nested_unwrap_error() -> None:
    with pytest.raises(ZeroDivisionError, match="^$"):
        raise UnwrapError(UnwrapError(ZeroDivisionError))


def test_unwrap_error_with_no_exception() -> None:
    error = UnwrapError("Oops...")
    with pytest.raises(UnwrapError, match="Oops..."):
        raise error

    assert isinstance(error.__error__.unwrap(), str)


def test_unwrap_error_with_exception() -> None:
    error = UnwrapError(LookupError("Oops, something went wrong..."))
    with pytest.raises(LookupError, match="Oops, something went wrong..."):
        raise error

    assert isinstance(error.__error__.unwrap(), LookupError)


def test_unwrap_error() -> None:
    error1 = UnwrapError(NameError())
    with pytest.raises(UnwrapError):
        raise error1

    assert isinstance(error1.__error__.unwrap(), NameError)

    error2 = UnwrapError("Error")
    with pytest.raises(UnwrapError, match="Error"):
        raise error2

    assert isinstance(error2.__error__.unwrap(), str)

    error3 = UnwrapError()
    with pytest.raises(UnwrapError, match="^$"):
        raise error3

    assert error3.__error__ == Nothing()
