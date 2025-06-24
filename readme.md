# fntypes

⚙️ Functional typing in Python!

```python
get_user()
  .then(get_posts)
  .map(lambda posts: sum(post.views for post in posts) / len(posts))
  .unwrap()
```

## why fntypes?

fntypes is based on the belief that raising exceptions should be avoided. So it defines a set of functional types needed to write better code. This type strategy grants you with higher control over your runtime.

Improving control flow will definitely result in avoiding logical errors and code readability. For example, you start to see each kind of behaviour you get from the function.

Panicking is the last recourse but for some obscure reason spawning exceptions each time you encounter something other than the all-successful behaviour became a norm in python code.

Let's fix this up and instead of panicking do treat error-state as equal to successful-state. fntypes provides you with all you need to migrate to functional typing approach

## (📖) documentation

See [documentation](/docs/index.md)

See [examples](/examples/)

## examples

```python
@unwrapping
def send_funds(
    sender_id: int, 
    receiver_id: int, 
    amount: decimal.Decimal,
) -> Result[TransactionID, str]:
    sender = get_user(sender_id).expect("Sender is undefined")
    receiver = get_user(receiver_id).expect("Receiver is undefined")
    if sender.get_balance().unwrap() < amount:
        return Error("Sender has not enough funds to complete transaction")
    
    return Ok(
        create_transaction(sender, receiver, amount)
        .unwrap()
        .transaction_id
    )
```

Contributions are welcome

MIT licensed

