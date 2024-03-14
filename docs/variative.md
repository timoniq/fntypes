# fntypes - Variative

`Variative` is a functional replacement for `Union` typehint. It has methods to enhance the control flow over union types. Some of these methods use head-tail notation due to the type-hinting restrictions.

Variative can contain multiple types (let the number of types be called N), therefore it can be contracted to N-1 states. Let's review the methods we can use to do so.

Head-tail notation is a notation that splits any set of data in two parts: head - the first element, and tail, that is a set of everything else. Therefore, if we consider a `Variative[A, B, C]`, its head will be `A`, and tail `[B, C]`.

## `.only(type = default to *head*)`

Only contracts the variative to a single type and returns a `Result[type, str]`

```python
x: Variative[A, B, C]

x.only(B) # Result[B, str]
x.only() # Result[A, str] (heading type of variative is A)
```

## `.detach()`

Head ensures that variative is not of *head* type and returns a result with a value-state of variative of *tail* types.

```python
x.detach()  # Result[Variative[B, C], str]
```

## `.v`

Returns a union (basically an intersection of all types of variative).

```python
x.v # Union[A, B, C]
```

