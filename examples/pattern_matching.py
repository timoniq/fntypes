from fntypes import Option, Variative, Some, unwrapping, Result, Ok, Nothing
from dataclasses import dataclass
import time

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


Event = Variative[Message, Call]

@unwrapping
def send_message(to_user: int, text: Option[str]) -> Result[int, "str"]:
    print("Sending message", repr(text.expect("text must be set")), f"to user #{to_user}")
    return Ok(int(time.time() % 1e5))


def process_event(event: Event) -> None:

    match event.v:
        case Message(from_user, Some(text)):
            send_message(from_user, Some("Hi. Thank you for your message " + repr(text)))
        case Message(from_user, _):
            send_message(from_user, Some("Hey, why you sent me an empty message?"))
        case Call(from_user):
            send_message(from_user, Some("Oh sorry I can't speak now"))


process_event(Event(Message(1, Some("Hi, friend!!!"))))
process_event(Event(Message(1, Nothing())))
process_event(Event(Call(1)))
