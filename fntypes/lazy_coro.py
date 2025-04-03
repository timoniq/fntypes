from __future__ import annotations

import typing

from fntypes.lazy import Lazy
from fntypes.tools import acache


class LazyCoro[Value]:
    __slots__ = ("_value",)

    def __init__(
        self,
        value: typing.Callable[[], typing.Coroutine[typing.Any, typing.Any, Value]],
        /,
    ) -> None:
        self._value = value

    @staticmethod
    def pure[T](value: T) -> LazyCoro[T]:
        async def wrapper() -> T:
            return value

        return LazyCoro(wrapper)

    def map[T](self, op: typing.Callable[[Value], T], /) -> LazyCoro[T]:
        async def wrapper() -> T:
            return op(await self())

        return LazyCoro(wrapper)

    def then[T](self, f: typing.Callable[[Value], typing.Awaitable[T]]) -> LazyCoro[T]:
        async def wrapper() -> T:
            return await f(await self())

        return LazyCoro(wrapper)

    def cache(self) -> LazyCoro[Value]:
        return LazyCoro(acache(self))

    def outer(self) -> Lazy[typing.Coroutine[typing.Any, typing.Any, Value]]:
        return Lazy(self)

    def __call__(self) -> typing.Coroutine[typing.Any, typing.Any, Value]:
        return self._value()

    def __await__(self) -> typing.Generator[typing.Any, None, Value]:
        return self().__await__()


__all__ = ("LazyCoro",)
