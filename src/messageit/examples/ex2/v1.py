
from abc import ABC, abstractmethod
from typing import Any

class Command(ABC):

    @abstractmethod
    def execute(self) -> Any:
        """Execute the command"""

class Event(ABC):

    @abstractmethod
    def handle(self) -> Any:
        """Handle event"""



from dataclasses import dataclass

@dataclass
class LoadFileCommand(Command):
    name: str = __file__

    def execute(self) -> Any:
        print(f"EXECUTE command: {self.name}")
        with open(self.name) as f:
            content = f.read()
        FileLoadedEvent(name=self.name, content=content).handle()
        return content


@dataclass
class FileLoadedEvent(Event):
    name: str
    content: str

    def handle(self) -> Any:
        print(f"HANDLE FileLoadedEvent: {self.name}")
    

def main():
    command = LoadFileCommand()
    command.execute()

if __name__ == "__main__":
    main()
