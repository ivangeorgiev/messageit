
from dataclasses import dataclass, field
from logging import Logger, getLogger, basicConfig
from typing import Any, DefaultDict
from uuid import UUID, uuid4
import inject


@dataclass
class Message:
    message_id: UUID = field(default_factory=uuid4, init=False)
    correlation_id: UUID = field(default_factory=uuid4)

@dataclass
class Command(Message):
    ...

class Event(Message):
    ...


@dataclass
class LoadFileCommand(Command):
    filename: str = __file__


@dataclass
class FileLoadedEvent(Event):
    filename: str = None
    size: int = None
    content: bytes = field(default=None, repr=False)

class CommandExecutor:
    executors: dict
    logger: Logger = getLogger(__name__)

    def __init__(self):
        self.executors = {}

    def execute(self, command: Command) -> Any:
        execute = self.executors.get(type(command), None)
        self.logger.debug(f"EXECUTE COMMAND: {command} with {execute}")
        if execute is None:
            raise ValueError(f"Handler not defined for {command}")
        return execute(command)

class EventHandler:
    observers: DefaultDict
    logger: Logger = getLogger(__name__)

    def __init__(self):
        self.observers = DefaultDict(list)

    def observe(self, event_type, observer):
        self.observers[event_type].append(observer)

    def handle(self, event: Event) -> Any:
        """Handle event"""
        self.logger.debug(f"HANDLE EVENT: {event}")
        for observe in self.observers[type(event)]:
            self.logger.debug(f"OBSERVE EVENT: {event} with {observe}")
            try:
                observe(event)
            except Exception as exception:
                self.logger.exception("Exception publishing event %s", exception)

class MessageProcessor:
    _commands: CommandExecutor
    _events: EventHandler

    @inject.autoparams()
    def __init__(self, commands: CommandExecutor, events: EventHandler) -> None:
        self._commands = commands
        self._events = events

    def process(self, message: Message) -> Any:
        if isinstance(message, Command):
            return self._commands.execute(message)
        return self._events.handle(message)
    
@inject.autoparams()
def load_file(cmd: LoadFileCommand, messages: MessageProcessor):
    with open(cmd.filename, "br") as f:
        content = f.read()
    event = FileLoadedEvent(correlation_id=cmd.correlation_id, filename=cmd.filename, size=len(content), content=content)
    messages.process(event)
    return content

def on_file_loaded(event: FileLoadedEvent):
    str(event)


@inject.autoparams()
def main(executor: CommandExecutor, handler: EventHandler, messages: MessageProcessor):
    basicConfig(level="DEBUG")
    # Configure file loading algorithm
    executor.executors[LoadFileCommand] = load_file
    # Configure file loaded event handling algorithm
    handler.observe(FileLoadedEvent, on_file_loaded)

    command = LoadFileCommand()
    messages.process(command)


def configure(binder: inject.Binder):
    binder.bind(CommandExecutor, CommandExecutor())
    binder.bind(EventHandler, EventHandler())
    
inject.configure(configure)

if __name__ == "__main__":
    main()
