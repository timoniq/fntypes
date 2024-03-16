from __future__ import annotations

import typing

from fntypes.result import Ok, Error

Value = typing.TypeVar("Value", covariant=True)
T = typing.TypeVar("T")
Err = typing.TypeVar("Err")


class Nothing(Error[None]):
    def __init__(self, *_suppress_args) -> None:
        super().__init__(None)
    
    def __repr__(self) -> str:
        return "Nothing()"
    
    def __del__(self):
        pass


class Some(typing.Generic[Value], Ok[Value]):
    def __repr__(self) -> str:
        return f"Some({self.value!r})"
    
    def map(self, op: typing.Callable[[Value], T], /) -> Some[T]:
        return Some(op(self.value))
    
    def and_then(self, f: typing.Callable[[Value], Option[T]]) -> Option[T]:
        return f(self.value)
    
    def __del__(self):
        pass


Option: typing.TypeAlias = Some[Value] | Nothing


__all__ = (
    "Nothing",
    "Some",
    "Option"
)
