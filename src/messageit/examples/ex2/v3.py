
from abc import ABC
from collections import defaultdict
from typing import Any, DefaultDict

class Command(ABC):
    ...

class Event(ABC):
    ...

class CommandExecutor:
    executors: dict

    def __init__(self):
        self.executors = {}

    def execute(self, command: Command) -> Any:
        execute = self.executors.get(type(command), None)
        if execute is None:
            raise ValueError(f"Handler not defined for {command}")
        return execute(command)

class EventHandler:
    observers: DefaultDict

    def __init__(self):
        self.observers = DefaultDict(list)

    def observe(self, event_type, observer):
        self.observers[event_type].append(observer)

    def handle(self, event: Event) -> Any:
        """Handle event"""
        for observe in self.observers[type(event)]:
            try:
                observe(event)
            except Exception as exception:
                self.logger.exception("Exception publishing event %s", exception)

from dataclasses import dataclass

@dataclass
class LoadFileCommand(Command):
    name: str = __file__


@dataclass
class FileLoadedEvent(Event):
    name: str
    content: str
    

def load_file(cmd: LoadFileCommand):
    print(f"EXECUTE load_file: {cmd.name}")
    with open(cmd.name) as f:
        content = f.read()
    handler.handle(FileLoadedEvent(name=cmd.name, content=content))
    return content

def on_file_loaded(event: FileLoadedEvent):
    print(f"HANDLE FileLoadedEvent: {event.name}")


def main():
    global handler
    executor = CommandExecutor()
    handler = EventHandler()
    # Configure file loading algorithm
    executor.executors[LoadFileCommand] = load_file
    # Configure file loaded event handling algorithm
    handler.observe(FileLoadedEvent, on_file_loaded)

    command = LoadFileCommand()
    executor.execute(command)

if __name__ == "__main__":
    main()
