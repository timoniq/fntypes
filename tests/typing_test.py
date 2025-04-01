import typing

from fntypes import Variative


def test_dunder_get_args() -> None:
    args = typing.get_args(Variative[int, str])
    assert len(args) == 2
    assert args[0] is int
    assert args[1] is str
