from fntypes import either, this, Error, Ok


def test_this() -> None:
    assert this(1) == 1


def test_either() -> None:
    assert (
        either(
            Ok(1),
            lambda: Ok(2),
        ).unwrap()
        == 1
    )

    assert (
        either(
            Error("oops"),
            lambda: Ok(10),
        ).unwrap()
        == 10
    )

    assert (
        either(
            Error("oops"),
            lambda: Error("shmoops"),
        ).unwrap_err()
        == "shmoops"
    )
