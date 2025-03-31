"""Common Objects for *all* import"""

from .error import UnwrapError
from .option import Nothing, Option, Some
from .result import RESULT_ERROR_LOGGER, Error, Ok, Result, Wrapped
from .tools.unwrapping import unwrapping
from .variative import Variative

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
