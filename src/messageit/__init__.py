"""

Example:
---------

Here is a complete example putting together event and message handling.

```python
from dataclasses import dataclass
from messageit import Command, Event, Executor, Publisher

@dataclass
class CleanMessage(Command):
    message: str = None

@dataclass
class MessageReceived(Event):
    message: str = None

def on_message_received(event: MessageReceived):
    print(f"Received message: {repr(event.message)}")
    clean_command = CleanMessage(message = event.message, correlation_id = event.message_id)
    cleaned = commands.handle(clean_command)
    print(f"Cleaned message: {repr(cleaned)}")

def clean_message(command: CleanMessage):
    return command.message.strip()

events = Publisher()
events.register(MessageReceived, on_message_received)

commands = Executor()
commands.register(CleanMessage, clean_message)

while True:
    print("Type your message or leave empty to exit and press <Enter>: ")
    message = input()
    if message == "":
        break
    result = events.handle(MessageReceived(message=message))
```
"""

from ._message import (
    Command,
    CommandExecutor,
    Event,
    EventPublisher,
    Executor,
    Handler,
    Message,
    ProxyHandler,
    Publisher,
)

__version__ = "0.1.1"
