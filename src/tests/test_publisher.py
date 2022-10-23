from unittest.mock import Mock
import pytest

from messageit import Publisher, SubscriptionPublisher
from messageit._registry import Registry, SimpleRegistry

class FakeMessage:
    ...

class TestSubscriptionPublisherClass:

    @pytest.fixture(name="publisher")
    def given_publisher(self):
        return SubscriptionPublisher()

    @pytest.fixture(name="handler")
    def given_handler(self):
        return Mock()

    @pytest.fixture(name="subscribed_handler")
    def given_subscribed_handler(self, publisher: Publisher, subject, handler):
        publisher.subscriptions.subscribe(subject, handler)
        return handler

    @pytest.fixture(name="subject")
    def given_subject(self):
        return FakeMessage

    @pytest.fixture(name="message")
    def given_message(self, subject):
        return subject()

    def test_new_instance(self, publisher):
        assert isinstance(publisher.subscriptions, Registry)
        assert isinstance(publisher.subscriptions, SimpleRegistry)

    def test_handle_calls_handlers_passing_message(self, publisher: Publisher, subscribed_handler: Mock, message: FakeMessage):
        publisher.publish(message)
        subscribed_handler.assert_called_once_with(message)

    def test_handle_returns_results(self, publisher: Publisher, subscribed_handler: Mock, message: FakeMessage):
        results = publisher.publish(message)
        assert results == [subscribed_handler.return_value]

    def test_handle_collects_exceptions(self, publisher: Publisher, subscribed_handler: Mock, message: FakeMessage):
        subscribed_handler.side_effect = ValueError
        results = publisher.publish(message)
        assert isinstance(results[0], ValueError)
    