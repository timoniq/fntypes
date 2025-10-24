from __future__ import annotations

import typing

from fntypes.library.error import UnwrapError
from fntypes.library.misc import identity, is_ok
from fntypes.library.monad.result import Result


class F[R, **P = [R]]:
    f: typing.Final[typing.Callable[P, R]]

    __slots__ = ("f",)

    @typing.overload
    def __init__[T](self: F[T, [T]], /) -> None: ...

    @typing.overload
    def __init__(self, f: typing.Callable[P, R], /) -> None: ...

    def __init__(self, f: typing.Any = identity, /) -> None:
        self.f = f

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.f(*args, **kwargs)

    def then[T](self, g: typing.Callable[[R], T], /) -> F[T, P]:
        return self.new(lambda *args, **kwargs: g(self.f(*args, **kwargs)))

    def ensure(
        self,
        chk: typing.Callable[[R], bool],
        error: typing.Callable[[R], BaseException] | BaseException | str | None = None,
    ) -> F[R, P]:
        if error is None:
            error = lambda _: UnwrapError()

        elif isinstance(error, str):
            e = error
            error = lambda _: UnwrapError(e)

        elif isinstance(error, BaseException):
            e = error
            error = lambda _: e

        def check(*args: P.args, **kwargs: P.kwargs) -> R:
            result = self.f(*args, **kwargs)
            if not chk(result):
                raise error(result)
            return result

        return self.new(check)

    def expect[T, Err](
        self: F[Result[T, Err], P],
        error: typing.Callable[[Result[T, Err]], BaseException] | BaseException | str | None = None,
    ) -> F[T, P]:
        return self.ensure(is_ok, error=error).then(lambda result: result.unwrap())
    
    if typing.TYPE_CHECKING:

        @typing.overload
        def new[T](self, /) -> F[T, [T]]: ...

        @typing.overload
        def new[X, **Y = [X]](self, f: typing.Callable[Y, X], /) -> F[X, Y]: ...

        def new(self, *args, **kwargs) -> typing.Any:
            ...
    else:
        def new(self, t) -> typing.Never:
            return self.__class__(t)


__all__ = ("F",)
