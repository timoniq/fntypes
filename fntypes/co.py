"""Common Objects for *all* import"""

from .option import Option, Some, Nothing
from .result import Result, Ok, Error, Wrapped
from .error import UnwrapError
from .variative import Variative
from .tools.unwrapping import unwrapping


__all__ = ("Option", "Some", "Nothing", "Result", "Ok", "Error", "Variative", "unwrapping", "Wrapped", "UnwrapError")
