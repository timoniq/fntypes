# fntypes - unwrapping

Unwrapping is a way to manage control flow designed with fntypes monads in a more convenient manner.

In theory, unwrapping is needed to create a syntaxic sugar that functions like `bind` method that defines a monad. In fntypes `bind` is known as `.and_then`. What it does, is it creates a binding between two functions returning a result of the same error type or option. If the current monad is in the state of error, the error is returned, if not, the value is passed into the function that is an argument in `and_then`. Let's look to the following example:

```python
def func1(a: int) -> Result[str, str]:
    if a == 0:
        return Error("a cannot be 0")
    return Ok(str(a))

def func2(a: int) -> Result[str, TypeError]:
    ...

def func3(b: str) -> Result[int, str]:
    if not b.isdigit():
        return Error("Not a digit")
    return Ok(int(b))


x: Result[int, str] = Ok(11)

x.and_then(func1) # "11"
x.and_then(func2) # Type checker: wrong error type
x.and_then(func1).and_then(func3) # 11

y: Result[int, str] = Error("Some error")

y.and_then(func1) # Error("Some error")
y.and_then(func1).and_then(func3) # Error("Some error")
```

Now, after we have understanding what `and_then` (or `bind`) is needed for, we can also comprehend the idea of a syntaxic sugar to apply this idea in a single scope, with no need to create multiple functions.

The only thing we should bear in mind is that the error type must be always same. For `Option` error type is None. If we need to change error type, we can use `expect` function.

In order to do that, `unwrapping` decorator is used:


```python
from fntypes import unwrapping, Result, Ok, Error, Option


class User:
    ...

    def get_balance(self) -> Result[decimal.Decimal, str]:
        ...


@dataclass
class Transaction:
    transaction_id: TransactionID


def get_user(sender_id: int) -> Option[User]:
    ...


def create_transaction(sender: User, receiver: User, amount: decimal.Decimal) -> Result[Transaction, str]:
    ...


@unwrapping
def send_funds(
    sender_id: int, 
    receiver_id: int, 
    amount: decimal.Decimal,
) -> Result[TransactionID, str]:
    sender = get_user(sender_id).expect("Sender is undefined") # marker 1
    receiver = get_user(receiver_id).expect("Receiver is undefined")
    if sender.get_balance().unwrap() < amount:  # marker 2
        return Error("Sender has not enough funds to complete transaction")
    
    return Ok(
        create_transaction(sender, receiver, amount)
        .unwrap()
        .transaction_id
    )
```

In this example we have a function which is wrapped in unwrapping decorator, it means that all methods like `unwrap`, `expect` are now covered and if any monad on which such methods are called is in the state of error, it will result in returning an error state out of the function obtaining the scope.

Let's look onto markers.

marker 1. Here we see that get_user returns an Option, which is of error type None, it doesn't correspond to an error type `str` of `Result[TransactionID, str]`. Thus, we have to change it and do `expect`. Into expect we pass the new error which is of type `str`. If error will pop out of `get_user`, an error will be immediately returned out of `send_funds`.

marker 2. Here, out of `get_balance` we get a result (`Result[decimal.Decimal, str]`) with a corresponding error type `str`. Thats the reason we can just do `unwrap`, and the error, if it appears, will be returned *as it is* out of the function `send_funds`.
