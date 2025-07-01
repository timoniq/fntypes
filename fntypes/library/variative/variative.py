import typing
from reprlib import recursive_repr

from fntypes.library.monad.result import Error, Ok, Result
from fntypes.utilities.runtime_generic import RuntimeGeneric

HEAD = typing.NewType("HEAD", type)


class Variative[*Ts](RuntimeGeneric):
    _value: typing.Any

    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    def __init__(self, value: typing.Any, /) -> None:
        self._value = value

    @recursive_repr()
    def __repr__(self) -> str:
        args = self.get_args()
        return "Variative{}({!r})".format(
            "[{}]".format(
                ", ".join(arg.__name__ if isinstance(arg, type) else repr(arg) for arg in args),
            )
            if args
            else "",
            self._value,
        )

    def __getitem__[T](self, __t: type[T]) -> Result[T, str]:
        return self.only(__t)

    @property
    def v(self) -> typing.Any:
        """Junction; intersection of Variative types."""

        return self._value

    def get_args(self) -> tuple[typing.Any, ...]:
        """>>> Variative[str, int].get_args()
        >>> (str, int)
        >>> Variative[str, int]("Hello!").get_args()
        >>> (str, int)
        """
        return self.__args__

    def only(self, t: typing.Any = HEAD) -> Result[typing.Any, str]:
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
            t = self.get_args()[0]

        if not isinstance(self._value, t):
            return Error(f"`{repr(self)}` cannot be set only to type `{t}`.")

        return Ok(self._value)

    def detach(self) -> typing.Any:
        """Detaches head type. To make this customizable Python must implement intersection typing.
        ```python
        v = Variative[str, int]

        v("Hello").detach() #> Error("Variative[str, int]('Hello') is of type <class 'str'>. Thus, head cannot be detached")

        v(1).detach() #> Ok(Variative[int](1))
        ```
        """

        args = self.get_args()
        if len(args) < 2:
            type_names = ", ".join(arg.__name__ if isinstance(arg, type) else repr(arg) for arg in args)
            return Error(f"Cannot detach head from Variative[{type_names}]: at least two args required.")

        head, *tail = args
        if isinstance(self._value, head) and not isinstance(self._value, tuple(tail)):
            return Error(f"`{repr(self)}` is of type `{head}`. Thus, head cannot be detached.")

        return Ok(Variative[*tail](self._value)) if tail else Ok(self._value)  # type: ignore[UnknownVariableType]


__all__ = ("Variative",)
