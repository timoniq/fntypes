import typing

from fntypes.result import Ok, Error, Result
from fntypes.option import Some, Nothing, Option


def this[T](obj: T, /) -> T:
    return obj


def either[T, Err](result: Result[T, Err], or_: typing.Callable[[], Result[T, Err]], /) -> Result[T, Err]:
    match result:
        case Ok(_):
            return result
        case _:
            return or_()


# Typeguards

def is_ok[T, Err](result: Result[T, Err]) -> typing.TypeGuard[Ok[T]]:
    return isinstance(result, Ok)


def is_err[T, Err](result: Result[T, Err]) -> typing.TypeGuard[Error[Err]]:
    return isinstance(result, Error)


def is_some[T](option: Option[T]) -> typing.TypeGuard[Some[T]]:
    return isinstance(option, Some)


def is_nothing[T](option: Option[T]) -> typing.TypeGuard[Nothing]:
    return isinstance(option, Nothing)


__all__ = (
    "this", 
    "either",
    "is_ok",
    "is_err",
    "is_some",
    "is_nothing",
)
