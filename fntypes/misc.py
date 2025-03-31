from fntypes.result import Result, Ok
import typing


def this[T](obj: T) -> T:
    return obj


def either[T, Err](result: Result[T, Err], or_: typing.Callable[[], Result[T, Err]]) -> Result[T, Err]:
    match result:
        case Ok(_):
            return result
        case _:
            return or_()


__all__ = (
    "this",
    "either",
)
