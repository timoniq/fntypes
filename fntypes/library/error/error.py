from __future__ import annotations

import typing
from functools import cached_property, lru_cache

from fntypes.utilities.misc import is_exception, to_exception_class

if typing.TYPE_CHECKING:
    from fntypes.library.monad.option import Option


@lru_cache
def to_catchable(base: type[Catchable], exception: type[BaseException], /) -> type[Catchable]:
    return type(exception.__name__, (base, exception), dict(__module__=exception.__module__))


def error_to_exception_args(error: typing.Any, /) -> tuple[object, ...]:
    if is_exception(error):
        return (error.args or (error,)) if not isinstance(error, type) else ()
    return () if error is None else (error,)


class Catchable(BaseException):
    pass


class UnwrapError[T](Catchable):
    def __new__(cls, error: T | None = None) -> typing.Self:
        if error is not None and is_exception(error) and (exception_class := to_exception_class(error)) is not cls:
            catchable = to_catchable(cls, exception_class)
            unwrap_error = typing.cast("typing.Self", super(cls, catchable).__new__(catchable))  # type: ignore
        else:
            unwrap_error = super().__new__(cls)

        unwrap_error.__dict__.update(dict(error_value=error))
        return unwrap_error

    def __init__(self, error: T | None = None) -> None:
        super().__init__(*error_to_exception_args(error))

    @cached_property
    def __error__(self) -> Option[typing.Any]:
        from fntypes.library.misc import from_optional

        return from_optional(self.__dict__["error_value"])


__all__ = ("UnwrapError",)
