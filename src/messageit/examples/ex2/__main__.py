"""
Use Dependency Injection with python-inject.

This is the same example as ex1, but uses Dependency Injection.
"""

from dataclasses import dataclass
from messageit import Command, Event, Executor, Publisher, EventPublisher, CommandExecutor

import inject

@dataclass
class CleanMessage(Command):
    message: str = None

@dataclass
class MessageReceived(Event):
    message: str = None

@inject.autoparams()
def on_message_received(event: MessageReceived, commands: CommandExecutor):
    print(f"Received message: {repr(event.message)}")
    clean_command = CleanMessage(message = event.message, correlation_id = event.message_id)
    cleaned = commands.handle(clean_command)
    print(f"Cleaned message: {repr(cleaned)}")

def clean_message(command: CleanMessage):
    return command.message.strip()


def configure_inject(binder: inject.Binder):
    binder.bind(EventPublisher, Publisher())
    binder.bind(CommandExecutor, Executor())

@inject.autoparams()
def main_loop(events: EventPublisher):
    while True:
        print("Enter your message:")
        message = input('> ')
        if message == "":
            break
        events.handle(MessageReceived(message=message))

@inject.autoparams()
def main(commands: CommandExecutor, events: EventPublisher):
    events.register(MessageReceived, on_message_received)
    commands.register(CleanMessage, clean_message)
    main_loop()

if __name__ == "__main__":
    inject.configure(configure_inject)
    main()
