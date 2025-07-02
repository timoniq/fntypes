import re

import pytest

from fntypes.library.error import UnwrapError
from fntypes.library.variative import Variative


def test_union_only_head() -> None:
    a = Variative[int, str](5)
    assert a.only().unwrap() == 5
    assert a.v == 5

    assert a[int].unwrap() == 5
    assert a[str].unwrap_or_none() == None

    b = Variative[int, str]("String")
    with pytest.raises(UnwrapError, match=re.escape("`Variative[int, str]('String')` cannot be set only to type `<class 'int'>`.")):
        b.only().unwrap()

    assert b.only().unwrap_or_none() is None


def test_union_only_custom() -> None:
    a = Variative[int, str, list]("String")
    assert a.only(str).unwrap() == "String"

    with pytest.raises(UnwrapError, match=re.escape("`Variative[int, str, list]('String')` cannot be set only to type `<class 'int'>`.")):
        a.only(int).unwrap()

    assert a.only(int).unwrap_or_none() is None
    assert a.only(dict).unwrap_or_none() is None


def test_union_detach():
    a = Variative[int, str]("String")
    assert a.detach().unwrap().v == "String"

    b = Variative[int, str](1)
    assert b.detach().unwrap_or_none() is None

    c = Variative[int, str, list]("String")
    detached = c.detach().unwrap()
    assert isinstance(detached, Variative)
    assert detached.get_args() == (str, list)

    with pytest.raises(UnwrapError):
        detached.detach().unwrap()


class C:
    pass


class A(C):
    pass


class B(C):
    pass


def test_union_detach_child() -> None:
    a = Variative[A, B, C](A())
    assert isinstance(a.detach().unwrap(), Variative)
    assert a.detach().unwrap().get_args() == (B, C)

    b = Variative[C, A, B](A())
    assert isinstance(b.detach().unwrap(), Variative)
    assert b.detach().unwrap().get_args() == (A, B)
    assert b.detach().unwrap().detach().unwrap_or_none() is None
