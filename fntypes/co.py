"""Common Objects for *all* import"""

from .error import UnwrapError
from .lazy import Lazy
from .lazy_coro import LazyCoro
from .lazy_coro_result import LazyCoroResult
from .option import Nothing, Option, Some
from .result import RESULT_ERROR_LOGGER, Error, Ok, Result, Wrapped
from .tools.unwrapping import unwrapping
from .variative import Variative

__all__ = (
    "RESULT_ERROR_LOGGER",
    "Option",
    "Some",
    "Lazy",
    "LazyCoro",
    "LazyCoroResult",
    "Nothing",
    "Result",
    "Ok",
    "Error",
    "Variative",
    "unwrapping",
    "Wrapped",
    "UnwrapError",
)
