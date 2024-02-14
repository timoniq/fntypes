from __future__ import annotations

import typing

from fntypes.result import Error, Ok, Result
from fntypes.tools import RuntimeGeneric

T = typing.TypeVar("T")
P = typing.TypeVar("P")
Ts = typing.TypeVarTuple("Ts")

HEAD = typing.NewType("HEAD", type)


class Variative(RuntimeGeneric, typing.Generic[*Ts]):
    def __init__(self: Variative[*tuple[T, ...]], value: T) -> None:
        self._value: typing.Any = value

    def __repr__(self) -> str:
        return "Variative[{}]({!r})".format(
            ", ".join(arg.__name__ if isinstance(arg, type) else repr(arg) for arg in self.get_args()),
            self._value,
        )
    
    @property
    def v(self: Variative[*tuple[T, ...]]) -> T:
        """Junction; intersection of Variative types."""

        return self._value

    @typing.overload
    def get_args(self) -> tuple[*Ts]:  # type: ignore
        """Overload `Variative.get_args`"""

    @typing.overload
    @classmethod
    def get_args(cls) -> tuple[*Ts]:
        """Overload `Proxy.get_args`"""
        
    def get_args(self) -> tuple[*Ts]:  # type: ignore
        return typing.get_args(self.__orig_class__)  # type: ignore

    @typing.overload
    def only(self, t: type[T]) -> Result[T, str]:
        # Probably there is not way for a better typing until T cannot be bound to Ts or intersection typehint is implemented
        ...

    @typing.overload
    def only(self: Variative[T, *tuple[P, ...]], t = HEAD) -> Result[T, str]:
        ...
    
    @typing.overload
    def only(self, t: type) -> Error[str]:
        # Will be in use when typing for the first overload will be improved
        ...

    def only(
        self: Variative[T, *tuple[T, ...]], 
        t: type = HEAD,
    ) -> Result[T, str]:
        """Sets `Variative` to single type. By default this type is generic leading type
        ```python
        u: Variative[str, int] = Variative("Hello")
        u.only() # Ok("Hello")
        u.only(str) # Ok("Hello")
        u.only(int) # Err
        u.only(list) # Err
        ```
        """

        if t == HEAD:
            t = self.get_args()[0]  # type: ignore
        if not isinstance(self._value, t):
            return Error(f"{repr(self)} cannot be set only to type {t}")
        return Ok(self._value)  # type: ignore
    
    @typing.overload
    def detach(self: Variative[P, T]) -> Ok[T]:
        ...

    @typing.overload
    def detach(self: Variative[P, *tuple[T, ...]]) -> Ok[Variative[T]]:
        ...

    @typing.overload
    def detach(self: Variative[P, *tuple[T, ...]]) -> Result[Variative[T], str]:
        ...
    
    def detach(self):
        """Detaches head type. To make this customizable Python must implement intersection typing
        ```python
        v = Variative[str, int]

        v("Hello").detach() #> Error("Variative[str, int]('Hello') is of type <class 'str'>. Thus, head cannot be detached")

        v(1).detach() #> Ok(Variative[int](1))
        ```
        """

        head, *tail = self.get_args()
        if isinstance(self._value, head) and not isinstance(self._value, tuple(tail)):  # type: ignore
            return Error(f"{repr(self)} is of type {head}. Thus, head cannot be detached")
        if len(self.get_args()) - 1 == 1:
            return Ok(self._value)
        return Ok(Variative[*self.get_args()[1:]](self._value))  # type: ignore


__all__ = ("Variative",)
