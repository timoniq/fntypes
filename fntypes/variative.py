from __future__ import annotations

import typing
from reprlib import recursive_repr

from fntypes.result import Error, Ok, Result
from fntypes.tools.runtime_generic import RuntimeGeneric

HEAD = typing.NewType("HEAD", type)


class Variative[*Ts](RuntimeGeneric):
    _value: typing.Any

    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    if typing.TYPE_CHECKING:

        def __new__[T](cls: type[Variative[*tuple[T, ...]]], value: T, /) -> Variative[*Ts]: ...

    else:

        def __init__(self, value, /) -> None:
            self._value = value

    @recursive_repr()
    def __repr__(self) -> str:
        args = self.get_args()
        return "Variative{}({!r})".format(
            "[{}]".format(
                ", ".join(arg.__name__ if isinstance(arg, type) else repr(arg) for arg in self.get_args()),
            )
            if args
            else "",
            self._value,
        )

    @property
    def v[T](self: Variative[*tuple[T, ...]]) -> T:
        """Junction; intersection of Variative types."""

        return self._value

    @typing.overload
    def get_args(self) -> tuple[*Ts]:  # type: ignore
        ...

    @typing.overload
    @classmethod
    def get_args(cls) -> tuple[*Ts]: ...

    def get_args(self) -> tuple[*Ts]:  # type: ignore
        """>>> Variative[str, int].get_args()
        >>> (str, int)
        >>> Variative[str, int]("Hello!").get_args()
        >>> (str, int)
        """

        return typing.get_args(getattr(self, "__orig_class__", self.__class__))

    @typing.overload
    def only[T](self, t: type[T]) -> Result[T, str]:
        # Probably there is not way for a better typing until T cannot be bound to Ts or intersection typehint is implemented
        ...

    @typing.overload
    def only[T, P](self: Variative[T, *tuple[P, ...]], t=HEAD) -> Result[T, str]: ...

    @typing.overload
    def only(self, t: type) -> Error[str]:
        # Will be in use when typing for the first overload will be improved
        ...

    def __getitem__[T](self, t: type[T]) -> Result[T, str]:
        return self.only(t)

    def only[T, P](  # type: ignore
        self: Variative[T, *tuple[P, ...]],
        t: type[T] = HEAD,
    ) -> Result[T, TypeError]:
        """Sets `Variative` to single type. By default this type is generic leading type.
        ```python
        v = Variative[str, int]("Hello")
        v.only() # Ok('Hello')
        v.only(str) # Ok('Hello')
        v.only(int) # Error("Variative[str, int]('Hello') cannot be set only to type <class 'int'>")
        v.only(list) # Error("Variative[str, int]('Hello') cannot be set only to type <class 'list'>")
        ```
        """
        if t is HEAD:
            t = self.get_args()[0]  # type: ignore

        if not isinstance(self._value, t):
            return Error(TypeError(f"`{repr(self)}` cannot be set only to type `{t}`."))

        return Ok(self._value)  # type: ignore

    @typing.overload
    def detach[P, T](self: Variative[P, T]) -> Ok[T]: ...

    @typing.overload
    def detach[P, T](self: Variative[P, *tuple[T, ...]]) -> Ok[Variative[T]]: ...

    @typing.overload
    def detach[P, T](
        self: Variative[P, *tuple[T, ...]],
    ) -> Result[Variative[T], TypeError]: ...

    def detach(self) -> typing.Any:
        """Detaches head type. To make this customizable Python must implement intersection typing.
        ```python
        v = Variative[str, int]

        v("Hello").detach() #> Error("Variative[str, int]('Hello') is of type <class 'str'>. Thus, head cannot be detached")

        v(1).detach() #> Ok(Variative[int](1))
        ```
        """

        head, *tail = self.get_args()
        if isinstance(self._value, head) and not isinstance(self._value, tuple(tail)):  # type: ignore
            return Error(TypeError(f"`{repr(self)}` is of type `{head}`. Thus, head cannot be detached."))

        if len(self.get_args()) - 1 == 1:
            return Ok(self._value)

        return Ok(Variative[*self.get_args()[1:]](self._value))  # type: ignore


__all__ = ("Variative",)
