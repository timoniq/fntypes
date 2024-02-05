# fntypes

Functional typing in Python!

See [examples](/examples/)

See [documentation](/docs/index.md)

fntypes is based on the belief that raising exceptions **should be avoided**. Therefore, it offers a set of functional types needed to write better code. This type strategy grants your project with higher control over type system - improves control flow

Contributions are welcome


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