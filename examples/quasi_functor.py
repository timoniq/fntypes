from fntypes import F, Result, Ok


def get_result(x: int) -> Result[int, str]:
    return Ok(x)


f = F[int]().then(get_result).then(lambda r: r.map_or(0, lambda x: x + 1)).expect()

print(f(1))  # 2
