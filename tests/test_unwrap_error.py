import pytest

from fntypes import UnwrapError


def test_unwrap_error_with_no_exception() -> None:
    error = UnwrapError("Oops...")
    with pytest.raises(UnwrapError, match="Oops..."):
        raise error

    assert isinstance(error.__error__, str)


def test_unwrap_error_with_exception() -> None:
    error = UnwrapError(LookupError("Oops, something went wrong..."))
    with pytest.raises(LookupError, match="Oops, something went wrong..."):
        raise error

    assert isinstance(error.__error__, LookupError)


def test_unwrap_error() -> None:
    error1 = UnwrapError(NameError())
    with pytest.raises(UnwrapError):
        raise error1

    assert isinstance(error1.__error__, NameError)

    error2 = UnwrapError("Error")
    with pytest.raises(UnwrapError, match="Error"):
        raise error2

    assert isinstance(error2.__error__, str)

    error3 = UnwrapError()
    with pytest.raises(UnwrapError, match="^$"):
        raise error3

    assert error3.__error__ == ()
