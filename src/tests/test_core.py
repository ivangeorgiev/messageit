from dataclasses import dataclass
from queue import Queue
from typing import Any, DefaultDict, List, Type
from messageit._core import DummyLogger, TypeRegistryResolver, MessageLoop
from messageit._protocols import LoggerProtocol, MessageHandlerProtocol, ResolverProtocol


class FakeTypeRegistryResolver(TypeRegistryResolver):
    @property
    def registry(self) -> DefaultDict[Type, List[MessageHandlerProtocol]]:
        return self._registry


@dataclass
class FakeMessage:
    id: int = 0


class FakeMessageLoop(MessageLoop):
    @property
    def logger(self) -> LoggerProtocol:
        return self._logger

    @property
    def resolver(self) -> ResolverProtocol:
        return self._resolver

    @property
    def queue(self) -> Any:
        return self._queue

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, value: bool):
        self._running = value


class TestTypeRegistryResolverClass:
    def test_when_new_instance_is_credated_then_registry_is_empty(self):
        r = FakeTypeRegistryResolver()
        assert len(r.registry.keys()) == 0

    def test_when_register_called_then_self_reference_is_returned(self):
        r = FakeTypeRegistryResolver()
        assert r.register(FakeMessage, lambda : 1) is r

    def test_when_register_handler_called_then_handler_is_in_registry(self):
        def fake_handler(message: Any) -> Any:
            return message

        r = FakeTypeRegistryResolver()
        r.register(FakeMessage, fake_handler)
        assert [fake_handler] == r.registry[FakeMessage]

    def test_when_register_multiple_handlers_then_all_handlers_are_in_registry(self):
        def fake_handler1(message: Any) -> Any:
            return message

        def fake_handler2(message: Any) -> Any:
            return message

        r = FakeTypeRegistryResolver()
        r.register(FakeMessage, fake_handler1)
        r.register(FakeMessage, fake_handler2)
        assert [fake_handler1, fake_handler2] == r.registry[FakeMessage]

    def test_resolve_returns_registered_handlers(self):
        def fake_handler1(message: Any) -> Any:
            return message

        def fake_handler2(message: Any) -> Any:
            return message

        r = FakeTypeRegistryResolver()
        r.register(FakeMessage, fake_handler1)
        r.register(FakeMessage, fake_handler2)
        assert [fake_handler1, fake_handler2] == r.resolve(FakeMessage())

    def test_resolve_returns_empty_list_no_registered_handlers(self):
        r = FakeTypeRegistryResolver()
        assert [] == r.resolve(FakeMessage())

class TestMessageLoopClass:

    def test_given_logger_not_provided_when_create_new_instance_then_logger_set_to_dummylogger(self):
        ml = FakeMessageLoop()
        assert isinstance(ml.logger, DummyLogger)

    def test_given_resolver_not_provided_when_create_new_instance_then_resolver_set_to_typeregistryresolver(self):
        ml = FakeMessageLoop()
        assert isinstance(ml.resolver, TypeRegistryResolver)

    def test_when_create_new_instance_then_queue_is_set(self):
        ml = FakeMessageLoop()
        assert isinstance(ml.queue, Queue)

    def test_when_create_new_instance_then_running_is_set_to_false(self):
        ml = FakeMessageLoop()
        assert not ml.running

    def test_given_running_is_true_when_call_stop_running_is_false(self):
        ml = FakeMessageLoop()
        ml.running = False
        ml.stop()
        assert not ml.running
