from __future__ import annotations

import typing

from fntypes.tools import cache


class Lazy[Value]:
    def __init__(self, value: typing.Callable[[], Value]) -> None:
        self._value = value

    @staticmethod
    def pure[T](value: T) -> Lazy[T]:
        return Lazy(lambda: value)

    def map[T](self, op: typing.Callable[[Value], T], /) -> Lazy[T]:
        return Lazy(lambda: op(self()))

    def cache(self) -> Lazy[Value]:
        return Lazy(cache(self))

    def __call__(self) -> Value:
        return self._value()


__all__ = ("Lazy",)
