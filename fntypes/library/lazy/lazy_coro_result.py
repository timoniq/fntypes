from __future__ import annotations

import typing
from typing import assert_never

from fntypes.library.caching import acache
from fntypes.library.lazy.lazy_coro import LazyCoro
from fntypes.library.monad.result import Error, Ok, Result
from fntypes.utilities.misc import Caster


class LazyCoroResult[Value, Err]:
    __slots__ = ("_value",)

    def __init__(
        self,
        value: typing.Callable[[], typing.Coroutine[typing.Any, typing.Any, Result[Value, Err]]],
        /,
    ) -> None:
        self._value = value

    @staticmethod
    def pure[T](value: T) -> LazyCoroResult[T, typing.Any]:
        async def wrapper() -> Result[T, typing.Any]:
            return Ok(value)

        return LazyCoroResult(wrapper)

    def unwrap(self) -> LazyCoro[Value]:
        async def wrapper() -> Value:
            return (await self()).unwrap()

        return LazyCoro(wrapper)

    def unwrap_err(self) -> LazyCoro[Err]:
        async def wrapper() -> Err:
            return (await self()).unwrap_err()

        return LazyCoro(wrapper)

    def unwrap_or[T](self, alternate_value: typing.Callable[[], typing.Awaitable[T]], /) -> LazyCoro[Value | T]:
        async def wrapper() -> Value | T:
            to_match = await self()
            match to_match:
                case Ok(value):
                    return value
                case Error(_):
                    return await alternate_value()
                case _:
                    assert_never(to_match)

        return LazyCoro(wrapper)

    def unwrap_or_none(self) -> LazyCoro[Value | None]:
        async def wrapper() -> Value | None:
            return (await self()).unwrap_or_none()

        return LazyCoro(wrapper)

    def unwrap_or_other[T](self, other: typing.Callable[[], typing.Awaitable[Result[T, Err]]], /) -> LazyCoro[Value | T]:
        async def wrapper() -> Value | T:
            to_match = await self()
            match to_match:
                case Ok(value):
                    return value
                case Error(_):
                    return (await other()).unwrap()
                case _:
                    assert_never(to_match)

        return LazyCoro(wrapper)

    def map[T](self, op: typing.Callable[[Value], T], /) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map(op)

        return LazyCoroResult(wrapper)

    def map_err[E](self, f: typing.Callable[[Err], E], /) -> LazyCoroResult[Value, E]:
        async def wrapper() -> Result[Value, E]:
            return (await self()).map_err(f)

        return LazyCoroResult(wrapper)

    def map_or[T](
        self,
        default_value: typing.Callable[[], typing.Awaitable[T]],
        f: typing.Callable[[Value], T],
        /,
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            to_match = await self()
            match to_match:
                case Ok(value):
                    return Ok(f(value))
                case Error(_):
                    return Ok(await default_value())
                case _:
                    assert_never(to_match)

        return LazyCoroResult(wrapper)

    def map_or_else[T](
        self,
        default_f: typing.Callable[[Err], T],
        f: typing.Callable[[Value], T],
        /,
    ) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            return (await self()).map_or_else(default_f, f)

        return LazyCoroResult(wrapper)

    def cast[T, F](
        self,
        ok: Caster[Value, T] = Ok,
        error: Caster[Err, F] = Error[Err],
        /,
    ) -> LazyCoro[T | F]:
        async def wrapper() -> T | F:
            return (await self()).cast(ok, error)

        return LazyCoro(wrapper)

    def expect(self, error: typing.Any, /) -> LazyCoro[Value]:
        async def wrapper() -> Value:
            return (await self()).expect(error)

        return LazyCoro(wrapper)

    def then[T](self, f: typing.Callable[[Value], typing.Awaitable[Result[T, Err]]], /) -> LazyCoroResult[T, Err]:
        async def wrapper() -> Result[T, Err]:
            to_match = await self()
            match to_match:
                case Ok(value):
                    return await f(value)
                case Error(err):
                    return Error(err)
                case _:
                    assert_never(to_match)

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
