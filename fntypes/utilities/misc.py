from __future__ import annotations

import inspect
import types
import typing

type Caster[T, R] = typing.Callable[[T], R] | type[type[T]]


def is_dunder(attr: str) -> bool:
    return attr.startswith("__") and attr.endswith("__")


def get_frame(depth: int = 0) -> types.FrameType | None:
    frame = inspect.currentframe()

    for _ in range(depth):
        if frame is not None:
            frame = frame.f_back

    return frame


class _GetArgsDescriptor[Instance, Attribute]:
    def __get__(self, instance: Instance | None, owner: type[Instance]) -> typing.Callable[[], tuple[typing.Any, ...]]:
        if instance is None:
            return getattr(owner, "get_args_cls")
        return types.MethodType(getattr(owner, "get_args_self"), instance)


class BindStaticMeta(type):
    def __new__(mcls: type["BindStaticMeta"], name: str, bases: tuple[type], namespace: dict[str, typing.Any]):
        if "get_args" in namespace:
            namespace["get_args"] = _GetArgsDescriptor()

        return super().__new__(mcls, name, bases, namespace)
