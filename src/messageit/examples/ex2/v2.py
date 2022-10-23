
from abc import ABC
from collections import defaultdict
from typing import Any, Callable

class Command(ABC):
    def execute(self) -> Any:
        """Execute the command"""
        self.executor()

    def executor(self) -> Any:
        pass

class Event(ABC):
    observers = defaultdict(list)

    @classmethod
    def observe(cls, observer):
        cls.observers[cls].append(observer)

    def handle(self) -> Any:
        """Handle event"""
        for observe in self.observers[self.__class__]:
            try:
                observe(self)
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
    FileLoadedEvent(name=cmd.name, content=content).handle()
    return content

def on_file_loaded(event: FileLoadedEvent):
    print(f"HANDLE FileLoadedEvent: {event.name}")


def main():
    # Configure file loading algorithm
    LoadFileCommand.executor = load_file
    # Configure file loaded event handling algorithm
    FileLoadedEvent.observe(on_file_loaded)

    command = LoadFileCommand()
    command.execute()

if __name__ == "__main__":
    main()
