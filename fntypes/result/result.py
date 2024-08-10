from __future__ import annotations

import typing

from fntypes.result.log_factory import ErrorLogFactoryMixin
from fntypes.error import UnwrapError
from reprlib import recursive_repr

T = typing.TypeVar("T")
Err = typing.TypeVar("Err", covariant=True)
Value = typing.TypeVar("Value", covariant=True)


def _default_ok(value: T) -> "Ok[T]":
    return Ok(value)


def _default_error(err: Err) -> "Error[Err]":
    return Error(err)


class Ok(typing.Generic[Value]):
    """`Result.Ok` representing success and containing a value."""

    __slots__ = ("_value",)
    __match_args__ = ("value",)

    def __init__(self, value: Value) -> None:
        self._value = value

    @recursive_repr()
    def __repr__(self) -> str:
        return f"<Result: Ok({self.value!r})>"

    def __bool__(self) -> typing.Literal[True]:
        return True
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ok):
            return False
        return self._value == other.value

    @property
    def value(self) -> Value:
        return self._value

    def unwrap(self) -> Value:
        return self._value

    def unwrap_or(self, alternate_value: object, /) -> Value:
        return self._value
    
    def unwrap_or_none(self) -> Value:
        return self._value

    def unwrap_or_other(self, other: object, /) -> Value:
        return self._value

    def map(self, op: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(op(self._value))

    def map_or(self, default_value: T, f: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(f(self._value))

    def map_or_else(self, default_f: object, f: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(f(self._value))
    
    def cast(self, ok: typing.Callable[[Value], T] = _default_ok, error: object = _default_error) -> T:
        return ok(self._value)

    def expect(self, error: typing.Any, /) -> Value:
        return self._value
    
    def and_then(self, f: typing.Callable[[Value], Result[T, Err]]) -> Result[T, Err]:
        return f(self._value)


class Error(typing.Generic[Err], ErrorLogFactoryMixin[Err]):
    """`Result.Error` representing error and containing an error value."""

    __slots__ = ("_error", "_tb", "_is_controlled")
    __match_args__ = ("error",)

    def __init__(self, error: Err) -> None:
        self._error = error
        self._tb: str | None = None
        self._is_controlled: bool = False
        super().__init__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Error):
            return False
        return self._error == other.error

    @recursive_repr()
    def __repr__(self) -> str:
        return (
            "<Result: Error({}: {!r})>".format(
                self._error.__class__.__name__,
                str(self._error),
            )
            if isinstance(self._error, BaseException)
            else f"<Result: Error({self._error!r})>"
        )
    
    def __bool__(self) -> typing.Literal[False]:
        return False

    @property
    def error(self) -> Err:
        return self._error

    def unwrap(self) -> typing.NoReturn:
        raise UnwrapError(self.error)

    def unwrap_or(self, alternate_value: T, /) -> T:
        return alternate_value
    
    def unwrap_or_none(self) -> None:
        return None

    def unwrap_or_other(self, other: Result[T, object], /) -> T:
        return other.unwrap()

    def map(self, op: object, /) -> typing.Self:
        return self

    def map_or(self, default_value: T, f: object, /) -> Ok[T]:
        return Ok(default_value)

    def map_or_else(self, default_f: typing.Callable[[Err], T], f: object, /) -> Ok[T]:
        return Ok(default_f(self._error))

    def expect(self, error: typing.Any, /) -> typing.NoReturn:
        raise UnwrapError(error)
    
    def and_then(self, f: typing.Callable[..., Result[T, Err]]) -> Error[Err]:
        return self
    
    def cast(self, ok: object = _default_ok, error: typing.Callable[[Err], T] = _default_error) -> T:
        return error(self._error)


Result: typing.TypeAlias = Ok[Value] | Error[Err]
Wrapped: typing.TypeAlias = Ok[Value] | Error[typing.Any]


__all__ = ("Ok", "Error", "Result", "Wrapped")
