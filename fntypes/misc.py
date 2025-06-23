import typing_extensions as typing

from fntypes.option import Nothing, Option, Some
from fntypes.result import Error, Ok, Result


def this[T](obj: T, /) -> T:
    return obj


def either[T, Err](result: Result[T, Err], or_: typing.Callable[[], Result[T, Err]], /) -> Result[T, Err]:
    match result:
        case Ok(_):
            return result
        case _:
            return or_()


def from_optional[Value](value: Value | None, /) -> Option[Value]:
    return Some(value) if value is not None else Nothing()


# Typeguards


def is_ok[T](result: Result[T, typing.Any], /) -> typing.TypeIs[Ok[T]]:
    return isinstance(result, Ok)


def is_err[Err](result: Result[typing.Any, Err], /) -> typing.TypeIs[Error[Err]]:
    return isinstance(result, Error)


def is_some[T](option: Option[T], /) -> typing.TypeIs[Some[T]]:
    return isinstance(option, Some)


def is_nothing(option: Option[typing.Any], /) -> typing.TypeIs[Nothing]:
    return isinstance(option, Nothing)


def is_dunder(attr: str) -> bool:
    return attr.startswith("__") and attr.endswith("__")


__all__ = (
    "this",
    "either",
    "is_ok",
    "is_err",
    "is_some",
    "is_nothing",
    "from_optional",
)
