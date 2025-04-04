from __future__ import annotations

import typing
from reprlib import recursive_repr

from fntypes.result import Error, Ok

T = typing.TypeVar("T")
Value = typing.TypeVar("Value", covariant=True)


class Nothing(Error[None]):
    def __init__(self, *_suppress_args: typing.Any) -> None:
        super().__init__(None)

    @recursive_repr()
    def __repr__(self) -> str:
        return "Nothing()"

    def __del__(self) -> None:
        pass

    def then(self, f: object, /) -> Nothing:
        return Nothing()


class Some(typing.Generic[Value], Ok[Value]):
    @recursive_repr()
    def __repr__(self) -> str:
        return f"Some({self._value!r})"

    def __del__(self) -> None:
        pass

    def map(self, op: typing.Callable[[Value], T], /) -> Some[T]:
        return Some(op(self._value))

    def then(self, f: typing.Callable[[Value], Option[T]], /) -> Option[T]:
        return f(self._value)


Option: typing.TypeAlias = Some[Value] | Nothing


__all__ = ("Nothing", "Some", "Option")
