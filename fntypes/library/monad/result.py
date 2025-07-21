from __future__ import annotations

import typing
from reprlib import recursive_repr

from fntypes.library.error import UnwrapError
from fntypes.utilities.log_factory import ErrorLogFactoryMixin
from fntypes.utilities.misc import Caster

if typing.TYPE_CHECKING:
    from fntypes.library.lazy.lazy_coro_result import LazyCoroResult

type AnyCallable = typing.Callable[[typing.Any], object]
type Result[T, E] = Ok[T] | Error[E]
type Wrapped[T] = Ok[T] | Error[typing.Any]


def _default_ok[T](value: T, /) -> Ok[T]:
    return Ok(value)


def _default_error[E](err: E, /) -> Error[E]:
    return Error(err)


class Ok[Value]:
    """`Result.Ok` representing success and containing a value."""

    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    @typing.overload
    def __init__(self: "Ok[None]") -> None:
        ...
    
    @typing.overload
    def __init__(self, value: Value) -> None:
        ...

    def __init__(self, value: Value = None) -> None:  # type: ignore
        self._value = value

    @recursive_repr()
    def __repr__(self) -> str:
        return f"<Result: Ok({self.value!r})>"

    def __bool__(self) -> typing.Literal[True]:
        return True

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._value == other.value

    @property
    def value(self) -> Value:
        return self._value

    def unwrap(self) -> Value:
        return self._value

    def unwrap_err(self) -> typing.NoReturn:
        raise UnwrapError("Ok has no an error.")

    def unwrap_or(self, alternate_value: typing.Any, /) -> Value:
        return self._value

    def unwrap_or_none(self) -> Value:
        return self._value

    def unwrap_or_other(self, other: typing.Any, /) -> Value:
        return self._value

    def map[T](self, op: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(op(self._value))

    def map_err(self, f: AnyCallable, /) -> Ok[Value]:
        return self

    def map_or[T](self, default_value: T, f: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(f(self._value))

    def map_or_else[T](self, default_f: AnyCallable, f: typing.Callable[[Value], T], /) -> Ok[T]:
        return Ok(f(self._value))

    def cast[T](
        self,
        ok: typing.Callable[[Value], T] = _default_ok,
        error: AnyCallable = _default_error,
        /,
    ) -> T:
        return ok(self._value)

    def expect(self, error: typing.Any, /) -> Value:
        return self._value

    def then[T, Err](self, f: typing.Callable[[Value], Result[T, Err]], /) -> Result[T, Err]:
        return f(self._value)

    def ensure[T, Err](self, chk: typing.Callable[[Value], bool], error: Err) -> Result[T, Err]:
        f: AnyCallable = lambda result: result if chk(self._value) else Error(error)
        return self.then(f)

    def to_async(self) -> LazyCoroResult[Value, typing.Any]:
        from fntypes.library.lazy.lazy_coro_result import LazyCoro, LazyCoroResult

        return LazyCoroResult(LazyCoro.pure(self))


class Error[E](ErrorLogFactoryMixin[E]):
    """`Result.Error` representing error and containing an error value."""

    __slots__ = ("_error", "_tb", "_is_controlled")
    __match_args__ = ("_error",)

    def __init__(self, error: E, /) -> None:
        self._error = error
        self._tb = None
        self._is_controlled = False
        super().__init__()

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
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
    def error(self) -> E:
        return self._error

    def unwrap(self) -> typing.NoReturn:
        raise UnwrapError(self.error)

    def unwrap_err(self) -> E:
        return self._error

    def unwrap_or[T](self, alternate_value: T, /) -> T:
        return alternate_value

    def unwrap_or_none(self) -> None:
        return None

    def unwrap_or_other[T](self, other: Result[T, object], /) -> T:
        return other.unwrap()

    def map(self, op: AnyCallable, /) -> typing.Self:
        return self

    def map_err[Err](self, f: typing.Callable[[E], Err], /) -> Error[Err]:
        return Error(f(self._error))

    def map_or[T](self, default_value: T, f: AnyCallable, /) -> Ok[T]:
        return Ok(default_value)

    def map_or_else[Err, T](self, default_f: typing.Callable[[E], T], f: AnyCallable, /) -> Ok[T]:
        return Ok(default_f(self._error))

    def expect(self, error: typing.Any, /) -> typing.NoReturn:
        raise UnwrapError(error)

    def then[T, Err](self, f: AnyCallable, /) -> Error[E]:
        return self

    def ensure(self, f: AnyCallable, error: E) -> Error[E]:
        return self

    def cast[T](
        self,
        ok: AnyCallable = _default_ok,
        error: Caster[E, T] = _default_error,
        /,
    ) -> T:
        return error(self._error)

    def to_async(self) -> LazyCoroResult[typing.Any, E]:
        from fntypes.library.lazy.lazy_coro_result import LazyCoro, LazyCoroResult

        return LazyCoroResult(LazyCoro.pure(self))


type Pulse[E] = Ok[None] | Error[E]

__all__ = ("Error", "Ok", "Result", "Wrapped", "Pulse")
