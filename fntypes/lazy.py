from __future__ import annotations

import typing

T = typing.TypeVar("T")
Value = typing.TypeVar("Value", covariant=True)


class Lazy(typing.Generic[Value]):
    def __init__(self, value: typing.Callable[[], Value]) -> None:
        self._value = value

    def map(self, op: typing.Callable[[Value], T], /) -> Lazy[T]:
        return Lazy(lambda: op(self()))

    def and_then(self, f: typing.Callable[[Value], Lazy[T]]) -> Lazy[T]:
        return Lazy(lambda: f(self())())

    def __call__(self) -> Value:
        return self._value()


__all__ = ("Lazy",)
