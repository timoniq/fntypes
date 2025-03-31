import asyncio
import typing
from functools import wraps

from fntypes.error import UnwrapError
from fntypes.option import Option
from fntypes.result import Error, Result

ParamSpec = typing.ParamSpec("ParamSpec")
T = typing.TypeVar("T")
Err = typing.TypeVar("Err")


@typing.overload
def unwrapping(
    func: typing.Callable[ParamSpec, Option[T]],
) -> typing.Callable[ParamSpec, Option[T]]: ...


@typing.overload
def unwrapping(
    func: typing.Callable[ParamSpec, Result[T, Err]],
) -> typing.Callable[ParamSpec, Result[T, Err]]: ...


@typing.overload
def unwrapping(
    func: typing.Callable[ParamSpec, typing.Awaitable[Option[T]]],
) -> typing.Callable[ParamSpec, typing.Coroutine[object, object, Option[T]]]: ...


@typing.overload
def unwrapping(
    func: typing.Callable[ParamSpec, typing.Awaitable[Result[T, Err]]],
) -> typing.Callable[ParamSpec, typing.Coroutine[object, object, Result[T, Err]]]: ...


def unwrapping(
    func: typing.Callable[ParamSpec, T],
) -> typing.Callable[ParamSpec, T]:
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def __call__(  # type: ignore
            *args: typing.Any,
            **kwargs: typing.Any,
        ):
            try:
                return await func(*args, **kwargs)
            except UnwrapError as e:
                return Error(e.__error__)  # type: ignore
    else:

        @wraps(func)
        def __call__(  # type: ignore
            *args: typing.Any,
            **kwargs: typing.Any,
        ):
            try:
                return func(*args, **kwargs)
            except UnwrapError as e:
                return Error(e.__error__)  # type: ignore

    return __call__  # type: ignore


__all__ = ("unwrapping",)
