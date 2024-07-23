import typing


class UnwrapError(TypeError):
    def __init__(self, err: typing.Any) -> None:
        self.err = err


__all__ = ("UnwrapError",)
