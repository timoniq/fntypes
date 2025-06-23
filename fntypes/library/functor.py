from __future__ import annotations

from collections.abc import Callable

import typing

from fntypes.library.error import UnwrapError
from fntypes.library.monad.result import Result
from fntypes.library.misc import is_ok


def identity[T](x: T, /) -> T:
    return x


class F[R, **P = [R]]:
    f: typing.Final[Callable[P, R]]

    @typing.overload
    def __init__[T](self: F[T, [T]], /) -> None: ...

    @typing.overload
    def __init__(self, f: Callable[P, R], /) -> None: ...

    def __init__(self, f: typing.Any = identity, /) -> None:
        self.f = f

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.f(*args, **kwargs)

    def then[T](self, g: Callable[[R], T], /) -> F[T, P]:
        return F(lambda *args, **kwargs: g(self.f(*args, **kwargs)))

    def must_be(
        self,
        chk: Callable[[R], bool],
        error: Callable[[R], BaseException] | BaseException | str | None = None,
    ) -> F[R, P]:
        if error is None:
            error = lambda _: UnwrapError()

        elif isinstance(error, str):
            error = lambda _: UnwrapError(error)

        elif isinstance(error, BaseException):
            e = error
            error = lambda _: e

        def check(*args: P.args, **kwargs: P.kwargs) -> R:
            result = self.f(*args, **kwargs)
            if not chk(result):
                raise error(result)
            return result

        return F(check)

    def expect[T, Err](
        self: "F[Result[T, Err], P]",
        error: Callable[[Result[T, Err]], BaseException] | BaseException | str | None = None,
    ) -> "F[T, P]":
        return self.must_be(lambda result: is_ok(result), error=error).then(lambda result: result.unwrap())


__all__ = ("F",)
