from fntypes.tools.unwrapping import unwrapping, UnwrapError
from fntypes.option import Option, Some, Nothing
from fntypes.result import Result, Ok, Error

def test_unwrapping():
    
    @unwrapping
    def unwrapped_func(x: Result[int, str]) -> Result[str, str]:
        value = x.unwrap()
        return Ok(str(value))
    
    assert unwrapped_func(Ok(1)) == Ok("1")
    assert unwrapped_func(Error("err")) == Error("err")

