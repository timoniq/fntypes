import pytest

from fntypes.library.monad.result import Error, Ok, Result
from fntypes.library.unwrapping import unwrapping


def test_unwrapping() -> None:
    @unwrapping
    def unwrapped_func(x: Result[int, str]) -> Result[str, str]:
        value = x.unwrap()
        return Ok(str(value))

    assert unwrapped_func(Ok(1)) == Ok("1")
    assert unwrapped_func(Error("err")) == Error("err")


@pytest.mark.asyncio
async def test_unwrapping_async() -> None:
    @unwrapping
    async def unwrapping_func(a: Result[int, str]) -> Result[float, str]:
        if a.unwrap() == 0:
            return Error("Cannot divide by 0")
        return Ok(10 / a.unwrap())

    assert await unwrapping_func(Ok(0)) == Error("Cannot divide by 0")
    assert (await unwrapping_func(Ok(3))).map(round).unwrap_or(0) == 3
