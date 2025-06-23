from __future__ import annotations
import types
import typing

Instance = typing.TypeVar("Instance")
Attribute = typing.TypeVar("Attribute")


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


def is_dunder(attr: str) -> bool:
    return attr.startswith("__") and attr.endswith("__")


type Caster[T, R] = typing.Callable[[T], R] | type[type[T]]
