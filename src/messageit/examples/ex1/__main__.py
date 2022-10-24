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

def main_loop():
    while True:
        print("Enter your message:")
        message = input('> ')
        if message == "":
            break
        events.handle(MessageReceived(message=message))

def main():
    global commands
    global events

    events = Publisher()
    commands = Executor()

    events.register(MessageReceived, on_message_received)
    commands.register(CleanMessage, clean_message)

    main_loop()

if __name__ == "__main__":
    main()
