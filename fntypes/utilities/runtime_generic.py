from __future__ import annotations

import inspect
import types
import typing
from functools import cached_property

from fntypes.utilities.misc import is_dunder

GENERIC_CLASS_ATTRS: typing.Final[set[str]] = set(dir(types.GenericAlias))


def bound_proxy(
    method: typing.Any,
    proxy: GenericProxy,
    /,
) -> typing.Any:
    def bound(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return method.__func__(proxy, *args, **kwargs)

    return bound


class GenericProxy:
    def __init__(self, generic: typing.Any) -> None:
        self._generic = generic

    def __getattr__(self, __name: str) -> typing.Any:
        if is_dunder(__name) or __name in GENERIC_CLASS_ATTRS:
            return getattr(self._generic, __name)

        obj = getattr(self._generic.__origin__, __name)

        if inspect.ismethod(obj) and hasattr(obj, "__self__") and isinstance(obj.__self__, type):
            return bound_proxy(obj, self)

        return obj

    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        if __name == "_generic":
            super().__setattr__(__name, __value)
        else:
            setattr(self._generic, __name, __value)

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self._generic(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} of {self._generic!r}>"

    @property
    @typing.no_type_check
    def __class__(self) -> type[types.GenericAlias]:
        return types.GenericAlias

    @cached_property
    def __args__(self) -> tuple[typing.Any, ...]:
        return self.get_args()

    def get_args(self) -> tuple[typing.Any, ...]:
        return typing.get_args(self._generic)


class RuntimeGeneric:
    @property
    def __args__(self) -> tuple[typing.Any, ...]:
        return typing.get_args(getattr(self, "__orig_class__", self.__class__))

    def __class_getitem__(cls, __key: typing.Any) -> typing.Any:
        class_getitem = getattr(super(RuntimeGeneric, cls), "__class_getitem__", None)
        if class_getitem is None:
            raise TypeError(f"Type `{cls.__name__}` is not subscriptable and it has no `__class_getitem__` method.")

        generic = class_getitem(__key)
        if any(typing.get_origin(arg) is not None for arg in typing.get_args(generic)):
            raise TypeError("Parametrized types are not supported.")

        return GenericProxy(generic) if getattr(generic, "__origin__", None) is not None else generic


__all__ = ("RuntimeGeneric", "GenericProxy")
