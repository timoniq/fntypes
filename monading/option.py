from __future__ import annotations

import typing

from monading.result import Ok, Error

Value = typing.TypeVar("Value", covariant=True)


class Nothing(Error[None]):
    def __init__(self) -> None:
        super().__init__(None)


class Some(typing.Generic[Value], Ok[Value]):
    pass


Option: typing.TypeAlias = Some[Value] | Nothing


__all__ = (
    "Nothing",
    "Some",
    "Option"
)
