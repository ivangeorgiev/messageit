# messageit
Message and Event Passing with Python

## Examples

### Create custom event

Custom events could be used to notify multiple subscribers about something that happened to the the application or to the world. To create custom event, you subclass the Event class and mark it as `dataclass`:

```python
from dataclasses import dataclass
from messageit import Event

@dataclass
class MessageReceived(Event):
    message: str = None
```

Each message has `message_id` property automatically set to an UUID. If you do not
pass `correlation_id` during message creation, `correlation_id` is set to the `message_id`.
The `correlation_id` could be used to track the execution of complex flows.

```python
event = MessageReceived(message="Hello world")
event.message_id   # UUID('ddeb3e81-3b75-403b-9b1e-13007b1f3abe')
event.correlation_id  # UUID('ddeb3e81-3b75-403b-9b1e-13007b1f3abe')
```

### Create custom command

Commands are used to perform actions. To create custom command, you subclass the Command class and mark it as `dataclass`:

```python
from dataclasses import dataclass
from messageit import Command

@dataclass
class CleanMessage(Command):
    message: str = None
```

If `correlation_id` is passed during message creation the passed value is set to the message's `correlation_id` attribute. With proper logging this could be used to track complex flows, e.g. distributed event and message handling.

```python
clean = CleanMessage(message="Hello world", correlation_id=event.correlation_id)
clean.message_id      # UUID('e0812459-5145-4de8-8d96-d0fce7fefb42')
clean.correlation_id  # UUID('ddeb3e81-3b75-403b-9b1e-13007b1f3abe')
event.correlation_id  # UUID('ddeb3e81-3b75-403b-9b1e-13007b1f3abe')
```

### Handle Commands - Assign algorithm to perform the action

Building on the previous example, we could assign algorithm to be executed when action is requested:

```python
from messageit import Executor

def clean_message(command: CleanMessage):
    return command.message.strip()

commands = Executor()
commands.register(CleanMessage, clean_message)

command = CleanMessage(message="   Hello   ")
commands.handle(command)   # 'Hello'
```

### Subscribe to Events - Get notified when event takes place 

Building on previous examples:

```python
from messageit import Publisher

def on_message_received(event: MessageReceived):
    clean_command = CleanMessage(message = event.message, correlation_id = event.message_id)
    cleaned = commands.handle(clean_command)
    print(f"Cleaned message: {repr(cleaned)}")


def echo_message(event: MessageReceived):
    print(f"Your input is: '{event.message}'")
    raise NotImplementedError()

events = Publisher()
events.register(MessageReceived, echo_message)
events.register(MessageReceived, on_message_received)

result = events.handle(
    MessageReceived(message="Hello World!!!")
)   # Your input is: 'Hello World!!!''
    # Cleaned message: 'Hello World!!!'
result  # [None, NotImplementedError()]
```

The two registered subscribers were called and produced output. The result from `handle()` is a collection from the results returned by subscribers invoked by `handle()`. If subscriber raised an exception, the exception is used as return result.

### Complete example

Here is a complete example putting all the pieces from above together. It is a simple command line applicationo that reads a line from the user and prints the cleansed message.

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

## Package and publish

To run the tests:

```bash
$ pytest
```

To package and publish:

```bash
$ pip install -U build twine
$ python -m build
$ python -m twine upload dist/*
```