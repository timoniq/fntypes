from __future__ import annotations

import typing
from functools import cached_property, lru_cache
from reprlib import recursive_repr

from fntypes.utilities.misc import is_exception, to_exception_class

if typing.TYPE_CHECKING:
    from fntypes.library.monad.option import Option


def repr_unwrap_error_value(
    error_value: Option[typing.Any],
    repr_func: typing.Callable[[typing.Any], str],
    /,
) -> str:
    return error_value.map(
        lambda error: str() if is_exception(error) and isinstance(error, type) else repr_func(error),
    ).unwrap_or("")


@lru_cache
def to_catchable(base: type[Catchable], exception: type[BaseException], /) -> type[Catchable]:
    return type(exception.__name__, (base, exception), dict(__module__=exception.__module__))


def error_to_exception_args(error: typing.Any, /) -> tuple[object, ...]:
    if is_exception(error):
        return (error.args or (error,)) if not isinstance(error, type) else ()
    return () if error is None else (error,)


def is_unwrap_error(error: typing.Any, /) -> bool:
    return is_exception(error) and issubclass(to_exception_class(error), UnwrapError)


class Catchable(BaseException):
    pass


class UnwrapError[T](Catchable):
    def __new__(cls, error: T | None = None) -> typing.Self:
        from fntypes.library.misc import from_optional

        if error is not None and is_exception(error) and (exception_class := to_exception_class(error)) is not cls:
            if not issubclass(exception_class, cls):
                catchable = to_catchable(cls, exception_class)
                unwrap_error = typing.cast("typing.Self", super(cls, catchable).__new__(catchable))  # pyright: ignore[reportArgumentType, reportUnknownMemberType]
            else:
                unwrap_error = super().__new__(exception_class)
        else:
            unwrap_error = super().__new__(cls)

        unwrap_error.__dict__.update(dict(__error__=from_optional(error)))
        return unwrap_error

    def __init__(self, error: T | None = None) -> None:
        Catchable.__init__(self, *error_to_exception_args(error))

    def __getattr__(self, __name: str) -> typing.Any:
        from fntypes.library.monad.option import Some

        match self.__error__:
            case Some(error) if isinstance(error, BaseException):
                if is_unwrap_error(error):
                    nested_error: typing.Any = error

                    while True:
                        err = nested_error.__error__.unwrap_or_none()

                        if err is None:
                            nested_error = None
                            break

                        nested_error = err
                        if not is_unwrap_error(err):
                            break

                    if nested_error is not None and isinstance(nested_error, BaseException):
                        return getattr(nested_error, __name)
                else:
                    return getattr(error, __name)
            case _:
                pass

        raise AttributeError(f"UnwrapError object has no attribute {__name!r}.")

    def __str__(self) -> str:
        return repr_unwrap_error_value(self.__error__, str)

    @recursive_repr()
    def __repr__(self) -> str:
        return repr_unwrap_error_value(self.__error__, repr)

    @cached_property
    def __error__(self) -> Option[typing.Any]:
        # The cached property is a version for getting an error value from the __dict__.
        # Raises ValueError if the error value is not defined.
        raise ValueError("UnwrapError has no error value.")


__all__ = ("UnwrapError",)
