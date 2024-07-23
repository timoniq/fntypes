"""Common Objects for *all* import"""

from .option import Option, Some, Nothing
from .result import RESULT_ERROR_LOGGER, Result, Ok, Error, Wrapped
from .error import UnwrapError
from .variative import Variative
from .tools.unwrapping import unwrapping

__all__ = (
    "RESULT_ERROR_LOGGER",
    "Option",
    "Some",
    "Nothing",
    "Result",
    "Ok",
    "Error",
    "Variative",
    "unwrapping",
    "Wrapped",
    "UnwrapError",
)
