from __future__ import annotations

from collections.abc import Callable
from typing import Any, Final, overload


def identity[T](x: T, /) -> T:
    return x


class F[R, **P = [R]]:
    f: Final[Callable[P, R]]

    @overload
    def __init__[T](self: F[T, [T]], /) -> None: ...

    @overload
    def __init__(self, f: Callable[P, R], /) -> None: ...

    def __init__(self, f: Any = identity, /) -> None:
        self.f = f

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.f(*args, **kwargs)

    def then[T](self, g: Callable[[R], T], /) -> F[T, P]:
        return F(lambda *args, **kwargs: g(self.f(*args, **kwargs)))


__all__ = ("F",)
