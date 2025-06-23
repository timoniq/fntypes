import inspect
import types
import typing

from fntypes.utilities.misc import is_dunder

GENERIC_CLASS_ATTRS = set(dir(types.GenericAlias))


class Proxy:
    def __init__(self, generic: typing.Any) -> None:
        self._generic = generic

    def __getattr__(self, __name: str) -> typing.Any:
        if is_dunder(__name) or __name in GENERIC_CLASS_ATTRS:
            return getattr(self._generic, __name)

        origin = self._generic.__origin__
        obj = getattr(origin, __name)

        if inspect.ismethod(obj) and hasattr(obj, "__self__") and isinstance(obj.__self__, type):
            def method_adapter(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                return obj.__func__(self, *args, **kwargs)

            return method_adapter

        return obj

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name == "_generic":
            super().__setattr__(name, value)
        else:
            setattr(self._generic, name, value)

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self._generic(*args, **kwargs)

    def get_args(self) -> tuple[type[typing.Any], ...]:
        return typing.get_args(self._generic)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} of {self._generic!r}>"

    @property
    @typing.no_type_check
    def __class__(self) -> type[types.GenericAlias]:
        return types.GenericAlias

    @property
    def __args__(self) -> tuple[type[typing.Any], ...]:
        return self.get_args()


class RuntimeGeneric:
    def __class_getitem__(cls, key: typing.Any) -> typing.Any:
        ancestor = super(RuntimeGeneric, cls)

        get_item_method = getattr(ancestor, "__class_getitem__", None)
        if get_item_method is None:
            raise TypeError(f"Type '{cls.__name__}' is not subscriptable and it has no __class_getitem__ method") from None

        generic = get_item_method(key)

        if any(typing.get_origin(arg) is not None for arg in typing.get_args(generic)):
            raise TypeError("Parametrized types are not supported.")

        if getattr(generic, "__origin__", None):
            return Proxy(generic)

        return generic


__all__ = ("Proxy", "RuntimeGeneric")
