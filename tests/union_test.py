import pytest
from monading import Union


def test_union_unwrap():
    assert Union[int, str](5).unwrap() == 5

def test_union_seclude_head():
    a = Union[int, str](5)
    assert a.seclude() == 5

    b = Union[int, str]("String")
    with pytest.raises(TypeError):
        b.seclude()
    
    assert b.seclude(raise_error=False) is None


def test_union_seclude_custom():
    a = Union[int, str, list[str]]("String")
    assert a.seclude(str) == "String"

    with pytest.raises(TypeError):
        a.seclude(int)
    
    assert a.seclude(int, raise_error=False) is None
    assert a.seclude(dict, raise_error=False) is None


def test_union_exclude():
    a = Union[int, str]("String")
    assert a.exclude(raise_error=False) == "String"
    
    b = Union[int, str](1)
    assert b.exclude(raise_error=False) is None
    
    c = Union[int, str, list]("String")
    excluded = c.exclude()
    assert isinstance(excluded, Union)
    assert excluded.get_args() == (str, list)

    with pytest.raises(TypeError):
        excluded.exclude()


class C:
    pass

class A(C):
    pass

class B(C):
    pass


def test_union_exclude_child():
    a = Union[A, B, C](A())
    assert isinstance(a.exclude(), Union)
    assert a.exclude().get_args() == (B, C)

    b = Union[C, A, B](A())
    assert isinstance(b.exclude(), Union)
    assert b.exclude().get_args() == (A, B)

    assert b.exclude().exclude(raise_error=False) is None
