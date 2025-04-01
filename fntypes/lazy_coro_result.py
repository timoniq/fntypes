from __future__ import annotations

import typing

from fntypes.lazy_coro import LazyCoro
from fntypes.tools import acache
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

    @staticmethod
    def pure(value: T) -> LazyCoroResult[T, typing.Any]:
        async def wrapper() -> Result[T, typing.Any]:
            return Ok(value)

        return LazyCoroResult(wrapper)

    def unwrap(self) -> LazyCoro[Value]:
        async def wrapper() -> Value:
            return (await self()).unwrap()

        return LazyCoro(wrapper)

    def unwrap_or(
        self, alternate_value: typing.Callable[[], typing.Awaitable[T]], /
    ) -> LazyCoro[Value | T]:
        async def wrapper() -> Value | T:
            match await self():
                case Ok(value):
                    return value
                case Error(_):
                    return await alternate_value()

        return LazyCoro(wrapper)

    def unwrap_or_none(self) -> LazyCoro[Value | None]:
        async def wrapper() -> Value | None:
            return (await self()).unwrap_or_none()

        return LazyCoro(wrapper)

    def unwrap_or_other(
        self, other: typing.Callable[[], typing.Awaitable[Result[T, Err]]], /
    ) -> LazyCoro[Value | T]:
        async def wrapper() -> Value | T:
            match await self():
                case Ok(value):
                    return value
                case Error(_):
                    return (await other()).unwrap()

        return LazyCoro(wrapper)

    def map(self, op: typing.Callable[[Value], T], /) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map(op)

        return LazyCoroResult(wrapper)

    def map_or(
        self,
        default_value: typing.Callable[[], typing.Awaitable[T]],
        f: typing.Callable[[Value], T],
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            match await self():
                case Ok(value):
                    return Ok(f(value))
                case Error(_):
                    return Ok(await default_value())

        return LazyCoroResult(wrapper)

    def map_or_else(
        self, default_f: typing.Callable[[Err], T], f: typing.Callable[[Value], T]
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map_or_else(default_f, f)

        return LazyCoroResult(wrapper)

    def cast(
        self,
        ok: typing.Callable[[Value], T] = Ok,
        error: typing.Callable[[Err], F] = Error,
    ) -> LazyCoro[T | F]:
        async def wrapper() -> T | F:
            return (await self()).cast(ok, error)

        return LazyCoro(wrapper)

    def expect(self, error: typing.Any, /) -> LazyCoro[Value]:
        async def wrapper() -> Value:
            return (await self()).expect(error)

        return LazyCoro(wrapper)

    def then(
        self, f: typing.Callable[[Value], typing.Awaitable[Result[T, Err]]]
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            match await self():
                case Ok(value):
                    return await f(value)
                case Error(err):
                    return Error(err)

        return LazyCoroResult(wrapper)

    def cache(self) -> LazyCoroResult[Value, Err]:
        return LazyCoroResult(acache(self))

    def outer(self) -> LazyCoro[Result[Value, Err]]:
        return LazyCoro(self)

    def __call__(self) -> typing.Coroutine[typing.Any, typing.Any, Result[Value, Err]]:
        return self._value()

    def __await__(self) -> typing.Generator[typing.Any, None, Result[Value, Err]]:
        return self().__await__()


__all__ = ("LazyCoroResult",)
