from fntypes import Result, Option, Error, Nothing, Some


def map_error(result: Result[int, str]) -> Option[int]:
    return result.cast(Some, Nothing)


def map_value(result: Result[int, str]) -> Result[str, str]:
    return result.map(str)


def map_or(result: Result[int, str]) -> int:
    return result.map_or(0, lambda x: x + 1).unwrap()


def get_n() -> Result[int, str]:
    return Error("Something happened")


n = get_n()

print(map_error(n))  # Nothing()
print(map_value(n)) # Error("Something happened")
print(map_or(n)) # 0
print(n.cast().cast().cast()) # Error("Something happened")