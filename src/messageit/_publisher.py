from abc import ABC, abstractmethod
from logging import Logger, getLogger
from typing import Any
from ._registry import Registry, SimpleRegistry

class Publisher(ABC):
    @abstractmethod
    def publish(self, message: Any):
        ...

class SubscriptionPublisher(Publisher):
    _subscriptions: Registry
    _logger: Logger

    def __init__(self):
        self._subscriptions = SimpleRegistry()
        self._logger = getLogger(__name__)

    def publish(self, message: Any):
        result = []
        for handler in self._subscriptions.subscribers_of(type(message)):
            try:
                self._logger.debug("handling event %s with handler %s", message, handler)
                result.append(handler(message))
            except Exception as exception:
                self._logger.exception("Exception handling event %s", message)
                result.append(exception)
        return result

    @property
    def subscriptions(self) -> Registry:
        return self._subscriptions
