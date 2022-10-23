from logging import getLogger
from typing import Any, DefaultDict, Hashable, List


class MessageBus:
    _topics: DefaultDict[Hashable, List]
    _logger: Any

    def __init__(self) -> None:
        self._topics = DefaultDict(list)
        self._logger = getLogger(__name__)

    @property
    def topics(self) -> List[Hashable]:
        """Returns a list of topics"""
        return self._topics.keys()

    def subscribe(self, topic: Hashable, observer: Any):
        self._topics[topic].append(observer)

    def subscribers(self, topic: Hashable):
        return self._topics[topic]

    def handle(self, message: Any):
        result = []
        for handler in self._topics[type(message)]:
            try:
                self._logger.debug("handling event %s with handler %s", message, handler)
                result.append(handler(message))
            except Exception as exception:
                self._logger.exception("Exception handling event %s", message)
                result.append(exception)
        return result
