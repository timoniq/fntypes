from fntypes.misc import this, either
from fntypes.result import Ok, Error


def test_this():
    assert this(1) == 1


def test_either():
    assert either(
        Ok(1),
        lambda: Ok(2),
    ).unwrap() == 1

    assert either(
        Error("oops"),
        lambda: Ok(10),
    ).unwrap() == 10

    assert either(
        Error("oops"),
        lambda: Error("shmoops"),
    ).error == "shmoops"
