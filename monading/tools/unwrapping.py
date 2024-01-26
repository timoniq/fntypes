import typing

from monading.result import Result, Error
from monading.option import Option, Nothing
from monading.protocols import UnwrapError

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
    
    return_t = typing.get_type_hints(func).get("return")

    if not return_t:
        raise TypeError("Function wrapped in unwrapping decorator must be type hinted with Result or Option return type")
    
    error_type: type | None = None
    
    if len(return_t.__args__) == 2 and return_t.__args__[1].__name__ == "Error":
        # Result type hint

        error_type = return_t.__args__[1].__args__[0]

    elif len(return_t.__args__) == 2 and return_t.__args__[0].__name__ == "Some":
        # Option type hint

        error_type = None
    
    else:
        raise TypeError("Return type hint should be either Result or Option in order to use unwrapping decorator")
    

    def __call__(*args, **kwargs) -> T:
        try: 
            return func(*args, **kwargs)
        except UnwrapError as e:

            # If error_type is None, error from unwrapping must be omitted
            if error_type is None:
                return Nothing  # type: ignore

            if not isinstance(e.err, error_type):
                raise TypeError(".unwrap() call of a result of incompatible error type")
                
            return Error(e.err)  # type: ignore
    return __call__  # type: ignore
