from __future__ import annotations

import dataclasses
import typing

from fntypes.result.log_factory import ErrorLogFactoryMixin
from fntypes.error import UnwrapError

T = typing.TypeVar("T")
Err = typing.TypeVar("Err", covariant=True)
Value = typing.TypeVar("Value", covariant=True)
ErrorType: typing.TypeAlias = str | BaseException | type[BaseException]


@dataclasses.dataclass(frozen=True, repr=False)
class Ok(typing.Generic[Value]):
    """`Result.Ok` representing success and containing a value."""

    value: Value

    def __repr__(self) -> str:
        return f"<Result: Ok({self.value!r})>"

    def __bool__(self) -> typing.Literal[True]:
        return True
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Ok):
            return False
        return self.value == other.value

    def unwrap(self) -> Value:
        return self.value

    def unwrap_or(self, alternate_value: object, /) -> Value:
        return self.unwrap()
    
    def unwrap_or_none(self) -> Value:
        return self.value

    def unwrap_or_other(self, other: object, /) -> Value:
        return self.value

    def map(self, op: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(op(self.value))

    def map_or(self, default: T, f: typing.Callable[[Value], T], /) -> T:
        return f(self.value)

    def map_or_else(self, default: object, f: typing.Callable[[Value], T], /) -> T:
        return f(self.value)

    def expect(self, error: ErrorType, /) -> Value:
        return self.value
    
    def and_then(self, f: typing.Callable[[Value], Result[T, Err]]) -> Result[T, Err]:
        return f(self.value)


@dataclasses.dataclass(repr=False)
class Error(typing.Generic[Err], ErrorLogFactoryMixin):
    """`Result.Error` representing error and containing an error value."""

    error: Err

    tb: str | None = None
    is_controlled: bool = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Error):
            return False
        return self.error == other.error

    def __repr__(self) -> str:
        return (
            "<Result: Error({}: {!r})>".format(
                self.error.__class__.__name__,
                str(self.error),
            )
            if isinstance(self.error, BaseException)
            else f"<Result: Error({self.error!r})>"
        )
    
    def __bool__(self) -> typing.Literal[False]:
        return False

    def unwrap(self) -> typing.NoReturn:
        raise (
            UnwrapError(self.error)
        )

    def unwrap_or(self, alternate_value: T, /) -> T:
        return alternate_value
    
    def unwrap_or_none(self) -> None:
        return None

    def unwrap_or_other(self, other: Result[T, object], /) -> T:
        return other.unwrap()

    def map(self, op: object, /) -> typing.Self:
        return self

    def map_or(self, default: T, f: object, /) -> T:
        return default

    def map_or_else(self, default: typing.Callable[[Err], T], f: object, /) -> T:
        return default(self.error)

    def expect(self, error: ErrorType, /) -> typing.NoReturn:
        raise error if not isinstance(error, str) else Exception(error)
    
    def and_then(self, f: typing.Callable[..., Result[T, Err]]) -> typing.Self:
        return self


Result: typing.TypeAlias = Ok[Value] | Error[Err]
Wrapped: typing.TypeAlias = Ok[Value] | Error[typing.Any]

__all__ = ("Ok", "Error", "Result")
