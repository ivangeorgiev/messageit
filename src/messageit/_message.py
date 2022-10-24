from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import Any, Callable, DefaultDict, List
from uuid import UUID, uuid4

@dataclass
class Message:
    message_id: UUID = field(default_factory=uuid4, init=False)
    correlation_id: UUID = field(default=None)

@dataclass
class Event(Message):
    """Event is a message which notifies the world that something has happened"""

@dataclass
class Command(Message):
    """Command is a request for action"""

class Handler(ABC):
    """Handle messages"""
    _logger: Logger = getLogger(__name__)

    @abstractmethod
    def handle(self, message: Any) -> Any:
        """Handle the message and returns the result"""


class CommandHandler(Handler):
    ...

class EventHandler(Handler):
    ...


class Executor(CommandHandler):
    """Handler which executes messages based on message type"""
    executors: dict

    def __init__(self):
        self.executors = {}

    def handle(self, message: Any) -> Any:
        """Executes a registered executor for the type of a message and returns result"""
        executor = self.executors.get(type(message), None)
        if executor is None:
            self._logger.error(f"EXECUTING: No handler defined for {type(message)}")
            raise ValueError(f"Handler not defined for {type(message)}")
        self._logger.debug(f"EXECUTING: {message} with {executor}")
        return executor(message)


class Publisher(EventHandler):
    """Handler which supports a list of subscribers per message type"""
    subscriptions: DefaultDict[Any, List[Callable]]

    def __init__(self):
        self.subscriptions = DefaultDict(list)

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
