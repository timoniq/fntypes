import pytest

from fntypes.error import UnwrapError


def test_unwrap_error_with_no_exception() -> None:
    error = UnwrapError("Oops...")
    with pytest.raises(UnwrapError, match="Oops..."):
        raise error

    assert isinstance(error.error, str)


def test_unwrap_error_with_exception() -> None:
    error = UnwrapError(LookupError("Oops, something went wrong..."))
    with pytest.raises(LookupError, match="Oops, something went wrong..."):
        raise error

    assert isinstance(error.error, LookupError)


def test_unwrap_error() -> None:
    error1 = UnwrapError(NameError())
    with pytest.raises(UnwrapError):
        raise error1
    
    assert isinstance(error1.error, NameError)

    error2 = UnwrapError("Error")
    with pytest.raises(UnwrapError, match="Error"):
        raise error2

    assert isinstance(error2.error, str)

    error3 = UnwrapError()
    with pytest.raises(UnwrapError, match=""):
        raise error3
    
    assert isinstance(error3.error, tuple)
