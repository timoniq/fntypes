from fntypes.tools import cache, acache


def test_cache():
    times_called = 0

    @cache
    def func() -> str:
        nonlocal times_called
        times_called += 1
        return "abc"

    assert func() == "abc"
    assert times_called == 1
    assert func() == "abc"
    assert times_called == 1


async def test_acache():
    times_called = 0

    @acache
    async def func() -> str:
        nonlocal times_called
        times_called += 1
        return "abc"

    assert await func() == "abc"
    assert times_called == 1
    assert await func() == "abc"
    assert times_called == 1
