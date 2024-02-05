import typing

from fntypes.result import Result, Error
from fntypes.option import Option
from fntypes.error import UnwrapError

ParamSpec = typing.ParamSpec("ParamSpec")
T = typing.TypeVar("T")
Err = typing.TypeVar("Err")


@typing.overload
def unwrapping(
    func: typing.Callable[ParamSpec, Option[T]],
) -> typing.Callable[ParamSpec, Option[T]]:
    ...


@typing.overload
def unwrapping(
    func: typing.Callable[ParamSpec, Result[T, Err]],
) -> typing.Callable[ParamSpec, Result[T, Err]]:
    ...


def unwrapping(
    func: typing.Callable[ParamSpec, T],
) -> typing.Callable[ParamSpec, T]:
    
    def __call__(*args, **kwargs) -> T:
        try: 
            return func(*args, **kwargs)
        except UnwrapError as e:
            return Error(e.err)  # type: ignore
    return __call__  # type: ignore
