from fntypes import Pulse, Ok, Error



def send_message(text: str) -> Pulse[str]:
    if not text:
        return Error("text is empty")
    return Ok()


result = send_message("hi!!!")

print(result)
