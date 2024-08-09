import typing


class UnwrapError(TypeError):
    __slots__ = ("err",)

    def __init__(self, err: typing.Any) -> None:
        self.err = err


__all__ = ("UnwrapError",)
