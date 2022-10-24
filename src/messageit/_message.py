from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import Any, Callable, DefaultDict, Hashable, List
from uuid import UUID, uuid4

@dataclass
class Message:
    message_id: UUID = field(default_factory=uuid4, init=False)
    correlation_id: UUID = field(default=None)

    def __post_init__(self):
        if self.correlation_id is None:
            self.correlation_id = self.message_id

@dataclass
class Event(Message):
    """Event is a message which notifies the world that something has happened"""

@dataclass
class Command(Message):
    """Command is a request for action"""

class Handler(ABC):
    """Abstract message handler
    
    Example:
    ---------

    In the following example we register a handler on `str` topic. The handler
    is invoked each time a `str` message is passed to the `handle` method.

    Also:
    
    - `handler` is a instance of some specific `Handler` implementation.
    - `on_text_message` is our message handler - a method with a single argument - the message

    >>> handler.register(str, on_text_message)
    >>> result = handler.handle("Hello")
    """
    _logger: Logger = getLogger(__name__)

    @abstractmethod
    def register(self, subject: Hashable, handler: Callable):
        """Register subject handler"""

    @abstractmethod
    def handle(self, message: Any) -> Any:
        """Handle the message and returns the result"""


class CommandHandler(Handler):
    """Abstract command handling class.
    
    Could be used for type-based dependency injection.
    """


class Executor(CommandHandler):
    """Handler which executes messages based on message type
    
    Example:
    --------

    Here is a complete example on command execution. We are implementing a command
    which does cleansing on raw text message, e.g. chat messages.

    ```python

    from dataclasses import dataclass
    from messageit import Executor, Command

    # Let's define a command class for message cleaning
    @dataclass
    class CleanMessage(Command):
        message: str = None

    # We also need an implementation of the cleaning algorithm.
    def clean_message(command: CleanMessage):
        return command.message.strip()

    # Create a command executor instance
    commands = Executor()
    # Associate the instances of CleanMessage command with our cleaning algorithm. 
    commands.register(CleanMessage, clean_message)

    # Now let's clean a message
    # Create a command with some message
    message = CleanMessage(message="    Hello     ")
    # Execute the command
    cleaned = commands.handle(message)
    # Inspect the result
    cleaned   # 'Hello'
    ```
    """
    executors: dict

    def __init__(self):
        self.executors = {}
        
    def register(self, subject: Hashable, handler: Callable):
        self.executors[subject] = handler

    def handle(self, message: Any) -> Any:
        """Executes a registered executor for the type of a message and returns result"""
        executor = self.executors.get(type(message), None)
        if executor is None:
            self._logger.error(f"EXECUTING: No handler defined for {type(message)}")
            raise ValueError(f"Handler not defined for {type(message)}")
        self._logger.debug(f"EXECUTING: {message} with {executor}")
        return executor(message)


class EventHandler(Handler):
    """Abstract event handling class.
    
    Could be used for type-based dependency injection.
    """
    ...

class Publisher(EventHandler):
    """Handler which supports a list of subscribers per message type
    
    Example:
    ---------

    ```python
    from messageit import Publisher
    
    publisher = Publisher()

    def on_text_message(event):
        print(f"EVENT: {event}")

    publisher.register(str, on_text_message)
    result = publisher.handle("Hello")   # EVENT: Hello
    result   # [None]
    ```
    """
    subscriptions: DefaultDict[Any, List[Callable]]

    def __init__(self):
        self.subscriptions = DefaultDict(list)

    def register(self, subject: Hashable, handler: Callable):
        self.subscriptions[subject].append(handler)

    def handle(self, message: Any) -> Any:
        """Invokes all subscribers to the type of a message and returns list of results"""
        result = []
        for handler in self.subscriptions[type(message)]:
            try:
                self._logger.debug("PUBLISHING %s with %s", message, handler)
                result.append(handler(message))
            except Exception as exception:
                self._logger.exception("EXCEPTION publishing %s", message)
                result.append(exception)
        return result
