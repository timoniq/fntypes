from __future__ import annotations

from collections.abc import Callable

from fntypes.library.caching import cache


class Lazy[Value]:
    def __init__(self, value: Callable[[], Value]) -> None:
        self._value = value

    @staticmethod
    def pure[T](value: T) -> Lazy[T]:
        return Lazy(lambda: value)

    def map[T](self, op: Callable[[Value], T], /) -> Lazy[T]:
        return Lazy(lambda: op(self()))

    def cache(self) -> Lazy[Value]:
        return Lazy(cache(self))

    def __call__(self) -> Value:
        return self._value()


__all__ = ("Lazy",)
