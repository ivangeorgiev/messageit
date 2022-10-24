from dataclasses import dataclass, field
from logging import Logger, getLogger, basicConfig
from typing import Any, DefaultDict
from uuid import UUID, uuid4
import inject

from messageit import Command, Event, CommandHandler, Executor, EventHandler, Publisher


@dataclass
class LoadFile(Command):
    filename: str = __file__


@dataclass
class FileLoaded(Event):
    filename: str = None
    content: bytes = field(repr=False, default=None)

@inject.autoparams()
def load_file(command: LoadFile, events: EventHandler):
    with open(command.filename, "br") as f:
        content = f.read()
    event = FileLoaded(
        correlation_id=command.correlation_id, filename=command.filename, content=content
    )
    events.handle(event)
    return content

@inject.autoparams()
def on_file_loaded(event: FileLoaded, logger: Logger):
    logger.info(f"FILE LOADED: {event.filename}")

def configure(binder: inject.Binder):
    binder.bind(CommandHandler, Executor())
    binder.bind(EventHandler, Publisher())
    binder.bind(Logger, getLogger(__name__))


@inject.autoparams()
def main(commands: CommandHandler, events: EventHandler, logger: Logger):
    basicConfig(level="DEBUG")
    #
    commands.register(LoadFile, load_file)
    events.register(FileLoaded, on_file_loaded)
    #
    load_command = LoadFile()
    content = commands.handle(load_command)
    logger.info(f"Load command returned {len(content)} bytes")


inject.configure(configure)

main()


if __name__ == "__main__":
    main()
