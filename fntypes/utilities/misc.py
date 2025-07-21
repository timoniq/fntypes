from __future__ import annotations

import inspect
import types
import typing

type Caster[T, R] = typing.Callable[[T], R]


def is_dunder(attr: str) -> bool:
    return attr.startswith("__") and attr.endswith("__")


def is_exception(obj: typing.Any, /) -> typing.TypeIs[BaseException | type[BaseException]]:
    return isinstance(obj, BaseException) or isinstance(obj, type) and issubclass(obj, BaseException)


def to_exception_class[T: BaseException](exception: T | type[T], /) -> type[T]:
    return exception if isinstance(exception, type) else type(exception)


def get_frame(depth: int = 0) -> types.FrameType | None:
    frame = inspect.currentframe()

    for _ in range(depth):
        if frame is not None:
            frame = frame.f_back

    return frame


__all__ = ("Caster", "get_frame", "is_dunder", "is_exception", "to_exception_class")
