from __future__ import annotations

import typing

from fntypes.result import Ok, Error

Value = typing.TypeVar("Value", covariant=True)
T = typing.TypeVar("T")


class Nothing(Error[None]):
    def __init__(self) -> None:
        super().__init__(None)
    
    def __repr__(self) -> str:
        return "Nothing()"


class Some(typing.Generic[Value], Ok[Value]):
    def __repr__(self) -> str:
        return f"Some({self.value!r})"
    
    def map(self, op: typing.Callable[[Value], T], /) -> Some[T]:
        return Some(op(self.value))


Option: typing.TypeAlias = Some[Value] | Nothing


__all__ = (
    "Nothing",
    "Some",
    "Option"
)
