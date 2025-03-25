from __future__ import annotations

import typing

from fntypes.lazy import Lazy

T = typing.TypeVar("T")
Value = typing.TypeVar("Value", covariant=True)


class LazyCoro(typing.Generic[Value]):
    def __init__(
        self,
        value: typing.Callable[[], typing.Coroutine[typing.Any, typing.Any, Value]],
    ) -> None:
        self._value = value

    def map(self, op: typing.Callable[[Value], T], /) -> LazyCoro[T]:
        async def wrapper() -> T:
            return op(await self())

        return LazyCoro(wrapper)

    def and_then(
        self, f: typing.Callable[[Value], typing.Callable[[], typing.Awaitable[T]]]
    ) -> LazyCoro[T]:
        async def wrapper() -> T:
            return await f(await self())()

        return LazyCoro(wrapper)

    def compose(self, f: typing.Callable[[Value], typing.Awaitable[T]]) -> LazyCoro[T]:
        async def wrapper() -> T:
            return await f(await self())

        return LazyCoro(wrapper)

    def outer(self) -> Lazy[typing.Coroutine[typing.Any, typing.Any, Value]]:
        return Lazy(self)

    def __call__(self) -> typing.Coroutine[typing.Any, typing.Any, Value]:
        return self._value()

    def __await__(self) -> typing.Generator[typing.Any, None, Value]:
        return self().__await__()


__all__ = ("LazyCoro",)
