from __future__ import annotations

import enum

import typing_extensions as typing

T = typing.TypeVar("T", default="NoError")


@enum.unique
class NoError(enum.Enum):
    NOERROR = enum.auto()


NOERROR: typing.Final[typing.Literal[NoError.NOERROR]] = NoError.NOERROR


def _is_exception(obj: typing.Any, /) -> bool:
    return (
        isinstance(obj, BaseException)
        or isinstance(obj, type)
        and issubclass(obj, BaseException)
    )


class _ErrorDescriptor(typing.Generic[T]):
    @typing.overload
    def __get__(
        self,
        instance: UnwrapError[NoError],
        owner: typing.Any,
    ) -> tuple[()]: ...

    @typing.overload
    def __get__(self, instance: UnwrapError[T], owner: typing.Any) -> T: ...

    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any: ...


class UnwrapError(typing.Generic[T], BaseException):
    if typing.TYPE_CHECKING:
        __error__: _ErrorDescriptor[T]

        @typing.overload
        def __init__(self) -> None: ...

        @typing.overload
        def __init__(self, error: T, /) -> None: ...

        def __init__(self, error: typing.Any = NOERROR) -> None: ...

        @typing.overload
        def __new__(cls) -> typing.Self: ...

        @typing.overload
        def __new__(cls, error: T, /) -> typing.Self: ...

        def __new__(cls, error: typing.Any = NOERROR) -> typing.Self: ...

    else:

        def __new__(cls, error=NOERROR, /):
            if _is_exception(error):
                err_args, err_class = (
                    (error.args, type(error))
                    if not isinstance(error, type)
                    else ((), error)
                )
                return type(
                    err_class.__name__,
                    (cls, err_class),
                    {"__module__": err_class.__module__},
                )(err_args)

            if not isinstance(error, tuple):
                error = (error,)

            return super().__new__(cls, *error)

        def __init__(self, error=NOERROR, /, *args):
            other_args = (
                ()
                if error is NOERROR or _is_exception(error) and isinstance(error, type)
                else (error,)
                if not isinstance(error, tuple)
                else error
            )
            super().__init__(
                *other_args
                if not _is_exception(error) or isinstance(error, type)
                else error.args,
                *args,
            )
            self.__error__ = () if error is NOERROR else error


__all__ = ("UnwrapError",)
