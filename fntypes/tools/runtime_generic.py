"""Implementation: https://github.com/python/typing/issues/629#issuecomment-829629259"""

import types
import typing
import inspect


class Proxy:
    def __init__(self, generic: typing.Any) -> None:
        object.__setattr__(self, "_generic", generic)

    def __getattr__(self, __name: str) -> typing.Any:
        generic_class_attrs = dir(typing._GenericAlias)  # type: ignore
        if (typing._is_dunder(__name) and generic_class_attrs) or (  # type: ignore
            __name in generic_class_attrs
        ):
            return getattr(self._generic, __name)
        origin = self._generic.__origin__
        obj = getattr(origin, __name)

        if inspect.ismethod(obj) and isinstance(obj.__self__, type):
            return lambda *a, **kw: obj.__func__(self, *a, *kw)
        else:
            return obj

    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        return setattr(self._generic, __name, __value)

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self._generic.__call__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} of {self._generic!r}>"

    def get_args(self) -> tuple[type[typing.Any], ...]:
        return typing.get_args(self._generic)

    @property
    def __class__(self) -> type[types.GenericAlias]:
        return typing._GenericAlias  # type: ignore

    @property
    def __args__(self) -> tuple[type[typing.Any], ...]:
        return self.get_args()


class RuntimeGeneric:
    def __class_getitem__(cls, __key: typing.Any) -> Proxy | typing.Any:
        generic = super().__class_getitem__(__key)  # type: ignore
        
        if any(typing.get_origin(arg) is not None for arg in typing.get_args(generic)):
            raise TypeError("Parametrized types are not supported.")
        
        if getattr(generic, "__origin__", None):
            return Proxy(generic)

        return generic


__all__ = ("Proxy", "RuntimeGeneric")
