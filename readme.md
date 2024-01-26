# monading

See [examples](/examples/)


```python3
from monading import Option, Union

@dataclass
class Message:
    from_user: int
    text: Option[str]

@dataclass
class PhotoMessage(Message):
    photo: str

@dataclass
class Call:
    from_user: int

Event = Union[Message, Call]


def process_event(event: Event):
    match event:

```