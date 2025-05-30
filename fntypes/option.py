from __future__ import annotations

import typing
from reprlib import recursive_repr

from fntypes.result import Error, Ok
from fntypes.tools.singleton import Singleton

type Option[T] = Some[T] | Nothing


class Nothing(Singleton, Error[None]):
    @typing.overload
    def __init__(self) -> None:
        pass

    @typing.overload
    def __init__(self, *suppress_args: typing.Any) -> None:
        pass

    def __init__(self, *_suppress_args: typing.Any) -> None:
        self._error = None
        self._tb = None
        self._is_controlled = False

    @recursive_repr()
    def __repr__(self) -> str:
        return "Nothing()"

    def __del__(self) -> None:
        pass

    def then(self, f: object, /) -> Nothing:
        return Nothing()


class Some[Value](Ok[Value]):
    @recursive_repr()
    def __repr__(self) -> str:
        return f"Some({self._value!r})"

    def __del__(self) -> None:
        pass

    def map[T](self, op: typing.Callable[[Value], T], /) -> Some[T]:
        return Some(op(self._value))

    def then[T](self, f: typing.Callable[[Value], Option[T]], /) -> Option[T]:
        return f(self._value)


__all__ = ("Nothing", "Some", "Option")
