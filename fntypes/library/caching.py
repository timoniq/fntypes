import collections.abc
import functools
import typing

from fntypes.library.monad.option import Nothing, Option, Some


def cache[T](func: collections.abc.Callable[[], T]) -> collections.abc.Callable[[], T]:
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


def acache[T](
    func: collections.abc.Callable[[], collections.abc.Coroutine[typing.Any, typing.Any, T]],
) -> collections.abc.Callable[[], collections.abc.Coroutine[typing.Any, typing.Any, T]]:
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


__all__ = ("acache", "cache")
