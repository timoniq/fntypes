import random

from fntypes import unwrapping, Option, Result, Some, Nothing, Ok, Error


@unwrapping
def calculate_something(arr: list[Option[int]]) -> Result[int, str]:
    if not arr[0].unwrap_or_none():
        return Error("Invalid first element")
    s = arr[0].unwrap()
    for coeff in arr[1:]:
        s += s * coeff.unwrap_or(0)
    return Ok(s)


@unwrapping
def calculate_over_something(x: Option[int], count: int) -> Option[int]:
    lst: list[Option[int]] = [x]
    for i in range(count):
        lst.append(Some(lst[len(lst) - 1].unwrap_or(0) + random.randint(15, 19)))
    return Some(calculate_something(lst).unwrap())


print(calculate_over_something(Some(10), 10).unwrap_or_none())  # *big number*
print(calculate_over_something(Nothing(), 10).unwrap_or_none())  # None
