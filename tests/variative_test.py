import pytest
from fntypes import Variative


def test_union_only_head():
    a = Variative[int, str](5)
    assert a.only().unwrap() == 5
    assert a.v == 5

    b = Variative[int, str]("String")
    with pytest.raises(TypeError):
        b.only().unwrap()
    
    assert b.only().unwrap_or_none() is None


def test_union_only_custom():
    a = Variative[int, str, list]("String")
    assert a.only(str).unwrap() == "String"

    with pytest.raises(TypeError):
        a.only(int).unwrap()
    
    assert a.only(int).unwrap_or_none() is None
    assert a.only(dict).unwrap_or_none() is None


def test_union_detach():
    a = Variative[int, str]("String")
    assert a.detach().unwrap() == "String"
    
    b = Variative[int, str](1)
    assert b.detach().unwrap_or_none() is None
    
    c = Variative[int, str, list]("String")
    detachd = c.detach().unwrap()
    assert isinstance(detachd, Variative)
    assert detachd.get_args() == (str, list)

    with pytest.raises(TypeError):
        detachd.detach().unwrap()


class C:
    pass

class A(C):
    pass

class B(C):
    pass


def test_union_detach_child():
    a = Variative[A, B, C](A())
    assert isinstance(a.detach().unwrap(), Variative)
    assert a.detach().unwrap().get_args() == (B, C)

    b = Variative[C, A, B](A())
    assert isinstance(b.detach().unwrap(), Variative)
    assert b.detach().unwrap().get_args() == (A, B)

    assert b.detach().unwrap().detach().unwrap_or_none() is None
