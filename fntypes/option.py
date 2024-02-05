from __future__ import annotations

import typing

from fntypes.result import Ok, Error

Value = typing.TypeVar("Value", covariant=True)


class Nothing(Error[None]):
    def __init__(self) -> None:
        super().__init__(None)
    
    def __repr__(self) -> str:
        return "<Option: Nothing()>"


class Some(typing.Generic[Value], Ok[Value]):
    def __repr__(self) -> str:
        return f"<Option: Some({self.value})>"


Option: typing.TypeAlias = Some[Value] | Nothing


__all__ = (
    "Nothing",
    "Some",
    "Option"
)
