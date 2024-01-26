from __future__ import annotations

import typing

from monading.protocols import Wrapped
from monading.tools import RuntimeGeneric

Ts = typing.TypeVarTuple("Ts")  # does not support bounds :(
Ps = typing.TypeVarTuple("Ps")
T = typing.TypeVar("T")
P = typing.TypeVar("P")

_ = typing.NewType("_", type)
HEAD = typing.NewType("HEAD", type)


class Union(RuntimeGeneric, typing.Generic[typing.Unpack[Ts]], Wrapped[typing.Union[typing.Unpack[Ts]]]):

    def __init__(self, value: typing.Union[typing.Unpack[Ts]]):
       self.value = value

    def __repr__(self) -> str:
        args = self.get_args()
        return "Union[{}]({})".format(", ".join([arg.__name__ for arg in args]), self.value)
    
    def unwrap(self) -> typing.Union[typing.Unpack[Ts]]:
        """Just returns ambiguous value"""
        return self.value
    
    def get_args(self):
       return typing.get_args(self.__orig_class__)  # type: ignore
    
    @typing.overload
    def seclude(self, t: type[T], *, raise_error: bool = True) -> T:
        # Probably there is not way for a better typing until T cannot be bound to Ts or intersection typehint is implemented
        ...

    @typing.overload
    def seclude(self: "Union[T, typing.Unpack[Ps]]", t = HEAD, *, raise_error: bool = True) -> T:
        ...
    
    @typing.overload
    def seclude(self, t: type, *, raise_error: bool = True) -> typing.NoReturn:
        # Will be in use when typing for the first overload will be improved
        ...

    def seclude(
        self: "Union[T, typing.Unpack[Ps]]", 
        t: type = HEAD,
        raise_error: bool = True,
    ) -> typing.Union[T, typing.Unpack[Ps], typing.NoReturn, None]:
        """Secludes union to single type. By default this type is generic leading type
        ```python
        u: Union[str, int] = Union("Hello")
        u.seclude() # "Hello"
        u.seclude(str) # "Hello"
        u.seclude(int) # TypeError
        u.seclude(list) # TypeError + (TODO: Unreachable code typehint)
        ```
        """
        if t == HEAD:
            t = self.get_args()[0]
        if not isinstance(self.value, t):
            if not raise_error:
                return None
            raise TypeError(f"{repr(self)} cannot be secluded to type {t}")
        return self.value  # type: ignore
    
    @typing.overload
    def exclude(
        self: "Union[P, T]",
        *,
        raise_error: bool = True,
    ) -> T:
        ...
    
    @typing.overload
    def exclude(
        self: "Union[T, typing.Unpack[Ps]]",
        *,
        raise_error: bool = True,
    ) -> "Union[typing.Unpack[Ps]]":
        ...

    @typing.overload
    def exclude(
        self: "Union[T, typing.Unpack[Ps]]", 
        raise_error: typing.Literal[False] = False,
    ) -> "Union[typing.Unpack[Ps]] | None":
        ...
    
    def exclude(  # type: ignore
        self,
        raise_error: bool = True,
    ):
        """Excludes head type. To make this customizable Python must implement intersection typing
        ```python
        u: Union[str, int]

        u = Union("Hello")
        u.exclude() # Union[str](value="Hello")

        u = Union(1)
        u.exclude() # TypeError
        ```
        """
        head, *tail = self.get_args()
        if isinstance(self.value, head) and not isinstance(self.value, tuple(tail)):
            if not raise_error:
                return None
            raise TypeError(f"{repr(self)} is of type {head}. thus, head cannot be excluded")
        if len(self.get_args()) - 1 == 1:
            return self.value
        return Union[*self.get_args()[1:]](self.value)  # type: ignore


__all__ = (
    "Union",
)
