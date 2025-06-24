from fntypes import Error, Ok, Result, Some, unwrapping


@unwrapping
def divide(a: Result[float, str], b: Result[float, str]) -> Result[float, str]:
    if b.unwrap() == 0:
        return Error("Division by zero")
    return Ok(a.unwrap() / b.unwrap())


result = divide(
    Some(10),
    divide(
        Some(4),
        divide(Some(5), Some(0)),
    ),
)

print(result)
