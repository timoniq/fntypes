import typing

from fntypes.library.monad.option import Option

class ErrorDescriptorProxy[T]:
    @typing.overload
    def __get__(
        self,
        instance: UnwrapError[typing.Literal[None]],
        owner: typing.Any,
    ) -> Option[typing.Any]: ...
    @typing.overload
    def __get__(self, instance: UnwrapError[T], owner: typing.Any) -> Option[T]: ...

class UnwrapError[T = None](BaseException):
    __error__: typing.Final[ErrorDescriptorProxy[T]]

    @typing.overload
    def __new__(cls) -> typing.Self: ...
    @typing.overload
    def __new__(cls, error: T, /) -> typing.Self: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, error: T, /) -> None: ...
