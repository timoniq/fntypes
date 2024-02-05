from __future__ import annotations

import typing

from fntypes.tools import RuntimeGeneric
from fntypes.result import Result, Ok, Error

Ts = typing.TypeVarTuple("Ts")  # does not support bounds :(
Ps = typing.TypeVarTuple("Ps")
T = typing.TypeVar("T")
P = typing.TypeVar("P")

_ = typing.NewType("_", type)
HEAD = typing.NewType("HEAD", type)

class Union(RuntimeGeneric, typing.Generic[typing.Unpack[Ts]]):

    def __init__(self, value: typing.Union[typing.Unpack[Ts]]):
       self.value = value

    def __repr__(self) -> str:
        args = self.get_args()
        return "Union[{}]({})".format(", ".join([arg.__name__ for arg in args]), self.value)
    
    @property
    def v(self) -> typing.Union[typing.Unpack[Ts]]:
        """Junction; intersection of union types"""
        return self.value
    
    @typing.overload
    @classmethod
    def get_args(cls) -> tuple[type, ...]:
        """overload Proxy.get_args"""

    @typing.overload
    def get_args(self) -> tuple[type, ...]:
        ...
    
    def get_args(self):  # type: ignore
       return typing.get_args(self.__orig_class__)  # type: ignore
        
    @typing.overload
    def only(self, t: type[T]) -> Result[T, str]:
        # Probably there is not way for a better typing until T cannot be bound to Ts or intersection typehint is implemented
        ...

    @typing.overload
    def only(self: "Union[T, typing.Unpack[Ps]]", t = HEAD) -> Result[T, str]:
        ...
    
    @typing.overload
    def only(self, t: type) -> Error[str]:
        # Will be in use when typing for the first overload will be improved
        ...

    def only(
        self: "Union[T, typing.Unpack[Ps]]", 
        t: type = HEAD,
    ) -> Result[typing.Union[T, typing.Unpack[Ps]], str]:
        """sets union to single type. By default this type is generic leading type
        ```python
        u: Union[str, int] = Union("Hello")
        u.only() # Ok("Hello")
        u.only(str) # Ok("Hello")
        u.only(int) # Err
        u.only(list) # Err
        ```
        """
        if t == HEAD:
            t = self.get_args()[0]
        if not isinstance(self.value, t):
            return Error(f"{repr(self)} cannot be set only to type {t}")
        return Ok(self.value)  # type: ignore
    
    @typing.overload
    def detach(
        self: "Union[P, T]",
    ) -> Ok[T]:
        ...
    
    @typing.overload
    def detach(
        self: "Union[T, typing.Unpack[Ps]]",
    ) -> Ok["Union[typing.Unpack[Ps]]"]:
        ...

    @typing.overload
    def detach(
        self: "Union[T, typing.Unpack[Ps]]", 
    ) -> Result["Union[typing.Unpack[Ps]]", str]:
        ...
    
    def detach(  # type: ignore
        self,
    ):
        """detaches head type. To make this customizable Python must implement intersection typing
        ```python
        u: Union[str, int]

        u = Union("Hello")
        u.detach() # Ok(Union[str](value="Hello"))

        u = Union(1)
        u.detach() # Err
        ```
        """
        head, *tail = self.get_args()
        if isinstance(self.value, head) and not isinstance(self.value, tuple(tail)):
            return Error(f"{repr(self)} is of type {head}. thus, head cannot be detached")
        if len(self.get_args()) - 1 == 1:
            return Ok(self.value)
        return Ok(Union[*self.get_args()[1:]](self.value))  # type: ignore
    


__all__ = (
    "Union",
)
