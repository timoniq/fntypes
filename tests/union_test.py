import pytest
from fntypes import Union


def test_union_only_head():
    a = Union[int, str](5)
    assert a.only().unwrap() == 5

    b = Union[int, str]("String")
    with pytest.raises(TypeError):
        b.only().unwrap()
    
    assert b.only().unwrap_or_none() is None


def test_union_only_custom():
    a = Union[int, str, list[str]]("String")
    assert a.only(str).unwrap() == "String"

    with pytest.raises(TypeError):
        a.only(int).unwrap()
    
    assert a.only(int).unwrap_or_none() is None
    assert a.only(dict).unwrap_or_none() is None


def test_union_detach():
    a = Union[int, str]("String")
    assert a.detach().unwrap() == "String"
    
    b = Union[int, str](1)
    assert b.detach().unwrap_or_none() is None
    
    c = Union[int, str, list]("String")
    detachd = c.detach().unwrap()
    assert isinstance(detachd, Union)
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
    a = Union[A, B, C](A())
    assert isinstance(a.detach().unwrap(), Union)
    assert a.detach().unwrap().get_args() == (B, C)

    b = Union[C, A, B](A())
    assert isinstance(b.detach().unwrap(), Union)
    assert b.detach().unwrap().get_args() == (A, B)

    assert b.detach().unwrap().detach().unwrap_or_none() is None
