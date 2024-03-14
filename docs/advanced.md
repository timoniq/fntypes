# fntypes - advanced

In order to use advanced methods, some theory needs to be explained.

Monad (a concept that fntypes is build on), requires its implementation to have a `bind` method. In `fntypes`, its name is `and_then` which expresses this idea in terms of imperative reality much better. We can *link* a monad (a result / an option) to a functor that will transform a value but preserve the original error type.

```python
x: Result[int, str]

def invalid_bind(value: int) -> Result[int, RuntimeError]:
    # Here, the error type is changed. Therefore, this binding procedure cannot be used with the `x` instance
    ...

def normal_bind(value: int) -> Result[int, str]:
    """Multiplies odd numbers by 2"""
    if x // 2 == 0:
        return Error("value cannot be even")
    return x * 2


x = Ok(3)

x.and_then(normal_bind) # Ok(6) ( Result[int, str] )
x.and_then(normal_bind).and_then(normal_bind)  # Error("value cannot be even")

x = Error("Something has already went wrong ..")

x.and_then(normal_bind) # Error("Something has already went wrong ..")
x.and_then(normal_bind).and_then(normal_bind) # Error("Something has already went wrong ..")
```
