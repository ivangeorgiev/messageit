from typing import Any, Hashable
from unittest.mock import Mock
import pytest
from messageit import MessageBus

class FakeMessage:
    pass

class TestMessageBusClass:
    @pytest.fixture(name="bus")
    def given_messagebus(self):
        return MessageBus()

    @pytest.fixture(name="topic")
    def given_topic(self):
        return FakeMessage

    @pytest.fixture(name="handler")
    def given_handler(self):
        return Mock()

    @pytest.fixture(name="subscribed_handler")
    def given_handler_is_subscribed(self, bus: MessageBus, topic: Any, handler: Any):
        bus.subscribe(topic, handler)
        return handler

    @pytest.fixture(name="message")
    def given_message(self, topic: Any):
        return topic()

    def test_create_new_instance_with_no_arguments(self):
        instance = MessageBus()
        assert isinstance(instance, MessageBus)

    def test_instance_topics_attribute(self, bus: MessageBus):
        assert list(bus.topics) == []

    def test_subscribe_observer(self, bus: MessageBus, topic: Hashable, handler: Mock):
        bus.subscribe(topic, handler)
        assert topic in bus.topics
        assert handler in bus.subscribers(topic)

    def test_handle_calls_handlers_passing_message(self, bus:MessageBus, subscribed_handler: Mock, message: FakeMessage):
        bus.handle(message)
        subscribed_handler.assert_called_once_with(message)

    def test_handle_returns_results(self, bus:MessageBus, subscribed_handler: Mock, message: FakeMessage):
        results = bus.handle(message)
        assert results == [subscribed_handler.return_value]

    def test_handle_collects_exceptions(self, bus:MessageBus, subscribed_handler: Mock, message: FakeMessage):
        subscribed_handler.side_effect = ValueError
        results = bus.handle(message)
        assert isinstance(results[0], ValueError)