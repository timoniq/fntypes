from __future__ import annotations

import enum

import typing_extensions as typing

T = typing.TypeVar("T", default="_NoDefault")


@enum.unique
class _NoDefault(enum.Enum):
    NODEFAULT = enum.auto()


NODEFAULT: typing.Final[typing.Literal[_NoDefault.NODEFAULT]] = _NoDefault.NODEFAULT


class _ErrorDescriptor(typing.Generic[T]):
    @typing.overload
    def __get__(self, instance: UnwrapError[_NoDefault], owner: typing.Any) -> tuple[()]: ...
    
    @typing.overload
    def __get__(self, instance: UnwrapError[T], owner: typing.Any) -> T: ...

    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any: ...
    

class UnwrapError(typing.Generic[T], BaseException):
    error: _ErrorDescriptor[T]

    if typing.TYPE_CHECKING:
        @typing.overload
        def __init__(self) -> None: ...

        @typing.overload
        def __init__(self, error: T) -> None: ...

        def __init__(self, error: typing.Any = NODEFAULT) -> None: ...

        @typing.overload
        def __new__(cls) -> typing.Self: ...

        @typing.overload
        def __new__(cls, error: T) -> typing.Self: ...

        def __new__(cls, error: typing.Any = NODEFAULT) -> typing.Self: ...

    else:
        def __new__(cls, error=NODEFAULT, /):
            if isinstance(error, BaseException) or (isinstance(error, type) and issubclass(error, BaseException)):
                err_args, err_class = (error.args, type(error)) if not isinstance(error, type) else ((), error)
                new_exception = type(
                    err_class.__name__,
                    (cls, err_class),
                    {"__module__": err_class.__module__},
                )(err_args)
                new_exception.error = () if error is NODEFAULT else error
                return new_exception

            err = error
            if not isinstance(error, tuple):
                error = (error,)

            exception = super().__new__(cls, *error)
            exception.error = err
            return exception


__all__ = ("UnwrapError",)
