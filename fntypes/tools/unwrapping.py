import asyncio
import typing
from functools import wraps

from fntypes.error import UnwrapError
from fntypes.option import Option
from fntypes.result import Error, Result

type Coroutine[T] = typing.Coroutine[typing.Any, typing.Any, T]


@typing.overload
def unwrapping[**P, R](
    func: typing.Callable[P, Option[R]],
    /,
) -> typing.Callable[P, Option[R]]: ...


@typing.overload
def unwrapping[**P, T, Err](
    func: typing.Callable[P, Result[T, Err]],
    /,
) -> typing.Callable[P, Result[T, Err]]: ...


@typing.overload
def unwrapping[**P, R](
    func: typing.Callable[P, typing.Awaitable[Option[R]]],
    /,
) -> typing.Callable[P, Coroutine[Option[R]]]: ...


@typing.overload
def unwrapping[**P, T, Err](
    func: typing.Callable[P, typing.Awaitable[Result[T, Err]]],
    /,
) -> typing.Callable[P, Coroutine[Result[T, Err]]]: ...


def unwrapping[**P, R](func: typing.Callable[P, R], /) -> typing.Callable[P, R]:
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def __call__(  # type: ignore  # noqa: N807
            *args: typing.Any,
            **kwargs: typing.Any,
        ):
            try:
                return await func(*args, **kwargs)
            except UnwrapError as e:
                return Error(e.__error__)  # type: ignore
    else:

        @wraps(func)
        def __call__(  # type: ignore  # noqa: N807
            *args: typing.Any,
            **kwargs: typing.Any,
        ):
            try:
                return func(*args, **kwargs)
            except UnwrapError as e:
                return Error(e.__error__)  # type: ignore

    return __call__  # type: ignore


__all__ = ("unwrapping",)
