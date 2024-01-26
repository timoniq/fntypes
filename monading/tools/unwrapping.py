import typing

from monading.result import Result, Error
from monading.protocols import UnwrapError

ParamSpec = typing.ParamSpec("ParamSpec")
T = typing.TypeVar("T")
Err = typing.TypeVar("Err")

def unwrapping(
    func: typing.Callable[ParamSpec, Result[T, Err]],
) -> typing.Callable[ParamSpec, Result[T, Err]]:
    
    result_t = typing.get_type_hints(func).get("return")
    if not result_t:
        raise TypeError("Function wrapped in unwrapping decorator must be type hinted with Result return type")
    
    error_type = result_t.__args__[1].__args__[0]

    def __call__(*args, **kwargs) -> Result[T, Err]:
        try: 
            return func(*args, **kwargs)
        except UnwrapError as e:
            if not isinstance(e.err, error_type):
                raise TypeError(".unwrap() call of a result of incompatible error type")
                
            return Error(e.err)
    return __call__
