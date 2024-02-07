# fntypes - option

`Option` is derived from [Result](/docs/result.md), but its error state is secluded to only one possible - the `Nothing` state. The value state of Option is called `Some`.
You may be used to use None python value to create such sort of ambiguation, but this is not good for the programming environment we are trying to create as it lacks functional features.
Due to the fact, that `Option` is derived from simple Result, we can use all of the features of Result in Option. We can create functional maps, unwrap variables and preserve control flow because of avoiding spawning exceptions what we would do, for example, in case when we would require variable not to be None in that paradigm we are trying to do away with.

In order to work with Option we will need to import such components as `Option`, `Some`, `Nothing`:

```python
from fntypes import Option, Some, Nothing
```

Let's create a function that will receive an option string and map its value into an uppercase version if it is in the state of `Some`:

```python
def shout(msg: Option[str]) -> None:
    print(msg.map(str.upper).unwrap_or("RRr"), "!!")

shout(Nothing())  # RRr !!
shout(Some("arseny"))  # ARSENY !!
```
