import pytest
from fntypes import Union


def test_union_seclude_head():
    a = Union[int, str](5)
    assert a.seclude().unwrap() == 5

    b = Union[int, str]("String")
    with pytest.raises(TypeError):
        b.seclude().unwrap()
    
    assert b.seclude().unwrap_or_none() is None


def test_union_seclude_custom():
    a = Union[int, str, list[str]]("String")
    assert a.seclude(str).unwrap() == "String"

    with pytest.raises(TypeError):
        a.seclude(int).unwrap()
    
    assert a.seclude(int).unwrap_or_none() is None
    assert a.seclude(dict).unwrap_or_none() is None


def test_union_exclude():
    a = Union[int, str]("String")
    assert a.exclude().unwrap() == "String"
    
    b = Union[int, str](1)
    assert b.exclude().unwrap_or_none() is None
    
    c = Union[int, str, list]("String")
    excluded = c.exclude().unwrap()
    assert isinstance(excluded, Union)
    assert excluded.get_args() == (str, list)

    with pytest.raises(TypeError):
        excluded.exclude().unwrap()


class C:
    pass

class A(C):
    pass

class B(C):
    pass


def test_union_exclude_child():
    a = Union[A, B, C](A())
    assert isinstance(a.exclude().unwrap(), Union)
    assert a.exclude().unwrap().get_args() == (B, C)

    b = Union[C, A, B](A())
    assert isinstance(b.exclude().unwrap(), Union)
    assert b.exclude().unwrap().get_args() == (A, B)

    assert b.exclude().unwrap().exclude().unwrap_or_none() is None
