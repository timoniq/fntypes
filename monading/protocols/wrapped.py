import typing


Value = typing.TypeVar("Value", covariant=True)
T = typing.TypeVar("T")


@typing.runtime_checkable
class Wrapped(typing.Protocol[Value]):

    def __eq__(self) -> bool:
        ...
    
    def __bool__(self) -> bool:
        ...

    def unwrap(self) -> Value:
        ...

    def unwrap_or(self, alternate_value: T, /) -> Value | T:
        ...

    def unwrap_or_other(self, other: "Wrapped[T]", /) -> Value | T:
        ...

    def unwrap_or_none(self) -> Value | None:
        ...

    def map(self, op: typing.Callable[[Value], T], /) -> "Wrapped[T]":
        ...

    def map_or(self, default: T, f: typing.Callable[[Value], T], /) -> T:
        ...

    def map_or_else(self, default: typing.Callable[[], T], f: typing.Callable[[Value], T], /) -> T:
        ...

    def expect(self, error: typing.Any, /) -> Value:
        ...


class UnwrapError(TypeError):
    def __init__(self, err):
        self.err = err
