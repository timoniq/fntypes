"""Common Objects for *all* import"""

from .option import Option, Some, Nothing
from .result import Result, Ok, Error, Wrapped
from .error import UnwrapError
from .union import Union
from .tools.unwrapping import unwrapping


__all__ = ("Option", "Some", "Nothing", "Result", "Ok", "Error", "Union", "unwrapping", "Wrapped", "UnwrapError")
