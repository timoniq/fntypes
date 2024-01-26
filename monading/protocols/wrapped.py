import typing


Value = typing.TypeVar("Value", covariant=True)


@typing.runtime_checkable
class Wrapped(typing.Protocol[Value]):
    def unwrap(self) -> Value:
        ...
