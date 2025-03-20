from __future__ import annotations

import typing

from fntypes.lazy_coro import LazyCoro
from fntypes.result import Ok, Error, Result

T = typing.TypeVar("T")
F = typing.TypeVar("F")
Err = typing.TypeVar("Err", covariant=True)
Value = typing.TypeVar("Value", covariant=True)


class LazyCoroResult(typing.Generic[Value, Err]):
    def __init__(
        self,
        value: typing.Callable[
            [], typing.Coroutine[typing.Any, typing.Any, Result[Value, Err]]
        ],
    ) -> None:
        self._value = value

    async def unwrap(self) -> Value:
        return (await self()).unwrap()

    async def unwrap_or(self, alternate_value: T, /) -> Value | T:
        return (await self()).unwrap_or(alternate_value)

    async def unwrap_or_none(self) -> Value | None:
        return (await self()).unwrap_or_none()

    async def unwrap_or_other(
        self,
        other: typing.Callable[
            [], typing.Coroutine[typing.Any, typing.Any, Result[T, Err]]
        ],
        /,
    ) -> Value | T:
        match await self():
            case Ok(value):
                return value
            case Error(_):
                return (await other()).unwrap()

    def map(self, op: typing.Callable[[Value], T], /) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map(op)

        return LazyCoroResult(wrapper)

    def map_or(
        self, default_value: T, f: typing.Callable[[Value], T]
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map_or(default_value, f)

        return LazyCoroResult(wrapper)

    def map_or_else(
        self, default_f: typing.Callable[[Err], T], f: typing.Callable[[Value], T]
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map_or_else(default_f, f)

        return LazyCoroResult(wrapper)

    async def cast(
        self,
        ok: typing.Callable[[Value], T] = Ok,
        error: typing.Callable[[Err], F] = Error,
    ) -> T | F:
        return (await self()).cast(ok, error)

    async def expect(self, error: typing.Any, /) -> Value:
        return (await self()).expect(error)

    def and_then(
        self, f: typing.Callable[[Value], LazyCoroResult[T, Err]]
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            match await self():
                case Ok(value):
                    return await f(value)()
                case Error(err):
                    return Error(err)

        return LazyCoroResult(wrapper)

    def outer(self) -> LazyCoro[Result[Value, Err]]:
        return LazyCoro(self)

    def __call__(self) -> typing.Coroutine[typing.Any, typing.Any, Result[Value, Err]]:
        return self._value()


__all__ = ("LazyCoroResult",)
