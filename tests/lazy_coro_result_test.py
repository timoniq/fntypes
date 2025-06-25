import pytest

from fntypes import LazyCoro
from fntypes.library.error import UnwrapError
from fntypes.library.monad.option import Nothing, Some
from fntypes.library.monad.result import Error, Ok, Result


async def inc_number(n: int) -> Result[int, TypeError]:
    return Ok(n + 1)


async def test_result_ok() -> None:
    result = Ok(1).to_async()
    assert await result.unwrap() == 1
    assert await result.unwrap_or(LazyCoro.pure(2)) == 1
    assert await result.unwrap_or_none() == 1
    assert await result.unwrap_or_other(LazyCoro.pure(Error(None))) == 1

    assert await result.map(lambda v: 22 / v) == Ok(22)
    assert await result.map_or(LazyCoro.pure(10), lambda v: v + v) == Ok(2)
    assert await result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == Ok(1)
    assert await result.then(inc_number).unwrap() == 2
    assert await result.expect("Should not happen") == 1
    assert isinstance(await result.cast(Some, Nothing), Some)
    assert (await result.cast(Some, Nothing)).unwrap() == 1


async def test_result_err() -> None:
    result = Error(TypeError("Oh")).to_async()
    with pytest.raises(TypeError):
        await result.unwrap()

    assert await result.unwrap_or(LazyCoro.pure(1)) == 1
    assert await result.unwrap_or_none() is None
    assert await result.unwrap_or_other(LazyCoro.pure(Ok(10))) == 10
    assert await result.map_or(LazyCoro.pure(5), lambda _: 6) == Ok(5)
    assert await result.map_or_else(lambda e: len(e.args[0]), lambda v: v) == Ok(2)
    assert (await result.then(inc_number)).unwrap_err().args[0] == "Oh"

    with pytest.raises(UnwrapError):
        await result.expect(ValueError())

    with pytest.raises(UnwrapError):
        (await result.cast(Some, Nothing)).unwrap()

    x = await result.cast(Some, Nothing)
    assert isinstance(x, Nothing)
    assert x.error is None
