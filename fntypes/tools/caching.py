import functools
import typing

from fntypes.option import Nothing, Some, Option

T = typing.TypeVar("T")
P = typing.ParamSpec("P")


def cache(func: typing.Callable[P, T]) -> typing.Callable[P, T]:
    cached: Option[T] = Nothing()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        nonlocal cached

        match cached:
            case Nothing():
                cached = Some(result := func(*args, **kwargs))
            case Some(result):
                pass

        return result

    return wrapper


def acache(
    func: typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, T]],
) -> typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, T]]:
    cached: Option[T] = Nothing()

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        nonlocal cached

        match cached:
            case Nothing():
                cached = Some(result := await func(*args, **kwargs))
            case Some(result):
                pass

        return result

    return wrapper


__all__ = ("cache", "acache")
