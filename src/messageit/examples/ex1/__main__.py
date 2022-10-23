from dataclasses import dataclass
import inject
from messageit import Publisher, Registry, SubscriptionPublisher

@dataclass
class GreatCommand:
    name: str

def say_hello(message: GreatCommand):
    print(f"Hello {message.name}")

def configure_bindings(binder: inject.Binder):
    handler = SubscriptionPublisher()
    binder.bind('handler', handler)
    binder.bind('handler_subscriptions', handler.subscriptions)

inject.configure(configure_bindings)

handler: Publisher = inject.instance("handler")
handlers: Registry  = inject.instance("handler_subscriptions")
handlers.subscribe(GreatCommand, say_hello)


handler.publish(GreatCommand(name="Joe"))


from logging import Logger, getLogger

class Command:
    executor: None
    logger: Logger = getLogger(__name__)

    def execute(self):
        self.executor(self)

class Event:
    observers = []
    logger: Logger = getLogger(__name__)

    def notify(self):
        for observe in self.observers:
            try:
                observe(self)
            except Exception as exception:
                self.logger.exception("Exception publishing event %s", self)
