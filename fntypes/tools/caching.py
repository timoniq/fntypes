import functools
import typing

from fntypes.option import Nothing, Some, Option

T = typing.TypeVar("T")


def cache(func: typing.Callable[[], T]) -> typing.Callable[[], T]:
    cached: Option[T] = Nothing()

    @functools.wraps(func)
    def wrapper() -> T:
        nonlocal cached

        match cached:
            case Nothing():
                cached = Some(result := func())
            case Some(result):
                pass

        return result

    return wrapper


def acache(
    func: typing.Callable[[], typing.Coroutine[typing.Any, typing.Any, T]],
) -> typing.Callable[[], typing.Coroutine[typing.Any, typing.Any, T]]:
    cached: Option[T] = Nothing()

    @functools.wraps(func)
    async def wrapper() -> T:
        nonlocal cached

        match cached:
            case Nothing():
                cached = Some(result := await func())
            case Some(result):
                pass

        return result

    return wrapper


__all__ = ("cache", "acache")
