"""Common Objects for *all* import"""

from .option import Option, Some, Nothing
from .result import Result, Ok, Error
from .union import Union
from .tools.unwrapping import unwrapping
from .protocols.wrapped import Wrapped


__all__ = ("Option", "Some", "Nothing", "Result", "Ok", "Error", "Union", "unwrapping", "Wrapped")
