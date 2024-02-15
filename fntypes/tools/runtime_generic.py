import typing
import inspect

# https://github.com/python/typing/issues/629#issuecomment-829629259


class Proxy:
  def __init__(self, generic):
    object.__setattr__(self, '_generic', generic)

  def __getattr__(self, name):
    generic_class_attrs = dir(typing._GenericAlias)  # type: ignore
    if (typing._is_dunder(name) and generic_class_attrs) or (name in generic_class_attrs):  # type: ignore
      return getattr(self._generic, name)
    origin = self._generic.__origin__
    obj = getattr(origin, name)
    if inspect.ismethod(obj) and isinstance(obj.__self__, type):
      return lambda *a, **kw: obj.__func__(self, *a, *kw)
    else:
      return obj

  def __setattr__(self, name, value):
    return setattr(self._generic, name, value)

  def __call__(self, *args, **kwargs):
    return self._generic.__call__(*args, **kwargs)

  def __repr__(self):
    return f'<{self.__class__.__name__} of {self._generic!r}>'
  
  def get_args(self) -> tuple[type, ...]:
    return typing.get_args(self._generic)
  
  @property
  def __class__(self):
    return typing._GenericAlias  # type: ignore
  
  @property
  def __args__(self):
    return self.get_args()

class RuntimeGeneric:
  def __class_getitem__(cls, key):
    generic = super().__class_getitem__(key)  # type: ignore
    if any(typing.get_origin(arg) is not None for arg in typing.get_args(generic)):
      raise TypeError('Parametrized types are not supported')
    if getattr(generic, '__origin__', None):
      return Proxy(generic)
    else:
      return generic
