# fntypes - Result

## Theory

`Result` is a key object needed to create names in two states: in a state of an error and in a state of a value.

Probably, you may be used to spawn exceptions as soon as you encounter an error. This is a bad practice. Fntypes advices strongly against raising exceptions. Why?

It's because they ruin control flow completely: exceptions, raised in a function, cannot be type-hinted, therefore we cannot see and guarantee to handle all the exceptions that appear from it. Thus, this makes us create abstract exception handlers *just in case*, which is definitely must be perceived as a bad practice.

In order to keep our control flow in a good form, we are offered to use Result monad - which is an entity that can obtain 2 states: a value - when the function proceeded successfully, or an error of a specific type - in case a function encountered a problem.

Therefore, two classes in `fntypes` exist to represent these states:

1. `fntypes.Ok` - representing a successful case

2. `fntypes.Error` - representing an error

An ambiguative state of those two states is called `Result`.

## Application

Let's create a function which is going to divide two numbers, and instead of raising an exception when the divisor is zero, its going to form an error state of a result. Otherwise, `Ok` with a resulting number is returned.

```python
from fntypes import Result, Ok, Error

# Result takes 2 type arguments:
# first one is a type of value on success,
# the second one is a type of error
def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Error("Divisor cannot be zero")
    return Ok(a / b)
```

Now, when the function is called, it returns a Result of one of two possible values. Let's try different ways of handling it:

```python
x = divide(6, 2) # <Result: Ok(3)>
y = divide(3, 0) # <Result: Error("Divisor cannot be zero")>

# Function unwrap, tranforms this call back to two states: of an exception or an actual value,
# Unless we are in a safe `unwrapped` scope.
x.unwrap() # 3
y.unwrap() # This is going to raise an exception: UnwrapError("Divisor cannot be zero")

# Unwrap with an alternative *value*
x.unwrap_or(10) # 3
y.unwrap_or(10) # 10

x.unwrap_or_none() # 3
y.unwrap_or_none() # None

# Unwrap with an alternative *result*
x.unwrap_or_other(divide(8, 4)) # <Result: Ok(3)>
y.unwrap_or_other(divide(8, 4)) # <Result: Ok(2)>

# Map - apply map on result value returning a result of an altered value type
# If result is in error state, mapper is not going to be applied
lst = ["Eniki", "Beniki", "Eli", "Vareniki"]

x.map(lambda n: lst[n]) # <Result: Ok("Vareniki")>
y.map(lambda n: lst[n]) # <Result: Error("Divisor cannot be zero")>

x.map(lambda n: lst[n]).map(str.upper) # <Result: Ok("VARENIKI")>

# More map functions are going to be presented in 'docs/advanced'

x.expect("Division failure") # Raises an exception: UnwrapError("Division failure")
# Expect is needed to transform error types

# .and_then - is an essential operation to compose multiple result returning functions
# Probably you may know it as bind operation
# Error type of those must be same !
# Argument is of value type, returning result can be of a different type
queue = []
IndexType = type("IndexType", (int,), {})

def send_to_queue(n: int) -> Result[int, str]:
    if len(queue) > 9:
        return Error("Too many numbers in queue!")
    queue.append(n)
    return Ok(len(queue) - 1) # index in queue

x.and_then(send_to_queue) # <Result: Ok(IndexType(0))>
x.and_then(send_to_queue).unwrap() # IndexType(1)
```
