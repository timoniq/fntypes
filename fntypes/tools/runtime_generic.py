import types
import typing
import inspect


GENERIC_CLASS_ATTRS = set(dir(typing._GenericAlias))  # type: ignore

class Proxy:
    def __init__(self, generic: typing.Any) -> None:
        self._generic = generic

    def __getattr__(self, __name: str) -> typing.Any:
        if (typing._is_dunder(__name) or __name in GENERIC_CLASS_ATTRS): # type: ignore
            return getattr(self._generic, __name)

        origin = self._generic.__origin__
        obj = getattr(origin, __name)

        if inspect.ismethod(obj) and hasattr(obj, '__self__') and isinstance(obj.__self__, type):
            return lambda *a, **kw: obj.__func__(self, *a, **kw)
        
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
    def __class__(self) -> type[types.GenericAlias]:
        return typing._GenericAlias  # type: ignore

    @property
    def __args__(self) -> tuple[type[typing.Any], ...]:
        return self.get_args()


class RuntimeGeneric:
    def __class_getitem__(cls, key: typing.Any) -> Proxy | typing.Any:
        generic = super().__class_getitem__(key)  # type: ignore

        if any(typing.get_origin(arg) is not None for arg in typing.get_args(generic)):
            raise TypeError("Parametrized types are not supported.")

        if getattr(generic, "__origin__", None):
            return Proxy(generic)
        
        return generic


__all__ = ("Proxy", "RuntimeGeneric")
