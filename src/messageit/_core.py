from queue import Queue
import queue
from typing import Any, DefaultDict, List, Mapping, Type
from ._protocols import MessageHandlerProtocol, ResolverProtocol, LoggerProtocol, KeyFunctionProtocol


class TypeRegistryResolver:
    _registry: DefaultDict[Type, List[MessageHandlerProtocol]]
    _key: KeyFunctionProtocol = type

    def __init__(self):
        self._registry = DefaultDict(list)

    def register(self, subject: Type, handler: MessageHandlerProtocol) -> 'TypeRegistryResolver':
        self._registry[subject].append(handler)
        return self

    def resolve(self, message: Any) -> List[MessageHandlerProtocol]:
        return self._registry[self._key(message)]

    def __call__(self, message: Any) -> List[MessageHandlerProtocol]:
        return self.resolve(message)


class DummyLogger:
    def debug(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        pass

    def info(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        pass

    def warning(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        pass

    def exception(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        pass

    def error(
        msg: object,
        *args: object,
        exc_info: Any = ...,
        stack_info: bool = ...,
        stacklevel: int = ...,
        extra: Mapping[str, object] | None = ...
    ) -> None:
        pass


class MessageLoop:
    _resolver: ResolverProtocol
    _logger: LoggerProtocol
    _queue: Queue
    _running: bool

    def __init__(self, resolver: ResolverProtocol = None, logger: LoggerProtocol = None):
        self._resolver = resolver or TypeRegistryResolver()
        self._logger = logger or DummyLogger()
        self._queue = Queue()
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            try:
                message = self._queue.get()
            except queue.Empty:
                continue
            for handler in self._resolver(message):
                #TODO handle exceptions from handler
                handler(message)


    def stop(self):
        self._running = False
