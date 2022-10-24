from unittest.mock import Mock
from uuid import UUID
import pytest

from messageit import Message, Command, Event, Executor, Publisher

class FakeMessage(Message):
    ...

class FakeCommand(Command):
    ...

class FakeEvent(Event):
    ...

class TestMessageClass:

    @pytest.fixture(name="message")
    def given_message(self):
        return FakeMessage()

    def test_message_id_is_auto_set(self, message: Message):
        assert isinstance(message.message_id, UUID)

    def test_correlation_id_is_none(self, message: Message):
        assert message.correlation_id is None


class TestExecutorClass:

    @pytest.fixture(name="handler")
    def given_handler(self):
        return Executor()

    @pytest.fixture(name="registered_executor")
    def given_registered_executor(self, handler: Executor):
        executor = Mock()
        handler.executors[FakeCommand] = executor
        return executor

    @pytest.fixture(name="handled_subject")
    def given_handled_subject(self, handler: Executor, registered_executor):
        return FakeCommand

    @pytest.fixture(name="handled_instance")
    def given_handled_subject(self, registered_executor):
        return FakeCommand()

    @pytest.fixture(name="unhandled_subject")
    def given_unhandled_subject(self):
        return Mock

    @pytest.fixture(name="unhandled_instance")
    def given_unhandled_instance(self, unhandled_subject):
        return unhandled_subject()


    def test_executors_map_is_empty(self, handler: Executor):
        assert handler.executors == {}

    def test_registered_executor_is_called(self, handler: Executor, registered_executor: Mock, handled_instance: FakeCommand):
        handler.handle(handled_instance)
        registered_executor.assert_called_once_with(handled_instance)

    def test_handle_returns_result_from_executor(self, handler: Executor, registered_executor: Mock, handled_instance: FakeCommand):
        result = handler.handle(handled_instance)
        assert result is registered_executor.return_value
    

    def test_handle_raises_valueerror_unregistered_subject(self, handler: Executor, unhandled_instance):
        with pytest.raises(ValueError):
            handler.handle(unhandled_instance)


class TestPublisherClass:

    @pytest.fixture(name="publisher")
    def given_publisher(self):
        return Publisher()

    @pytest.fixture(name="subscribers")
    def given_subscribers(self, publisher: Publisher):
        subscriber1 = Mock()
        publisher.subscriptions[FakeEvent].append(subscriber1)
        subscriber2 = Mock()
        publisher.subscriptions[FakeEvent].append(subscriber2)
        return [subscriber1,subscriber2]

    @pytest.fixture(name="subscriber1")
    def given_subscriber1(self, subscribers):
        return subscribers[0]

    @pytest.fixture(name="subscriber2")
    def given_subscriber2(self, subscribers):
        return subscribers[1]


    @pytest.fixture(name="subscribed_subject")
    def given_subscribed_subject(self, subscribers):
        return FakeEvent

    @pytest.fixture(name="subscribed_instance")
    def given_subscribed_instance(self, subscribed_subject):
        return subscribed_subject()

    
    def test_no_subscriptions(self, publisher: Publisher):
        assert len(publisher.subscriptions.keys()) == 0
        assert len(publisher.subscriptions) == 0

    def test_subscribers_are_notified(self, publisher: Publisher, subscriber1: Mock, subscriber2: Mock, subscribed_instance):
        publisher.handle(subscribed_instance)
        subscriber1.assert_called_once_with(subscribed_instance)
        subscriber2.assert_called_once_with(subscribed_instance)

    def test_handle_returns_list_of_results(self, publisher: Publisher, subscriber1: Mock, subscriber2: Mock, subscribed_instance):
        result = publisher.handle(subscribed_instance)
        assert result == [subscriber1.return_value, subscriber2.return_value]


    def test_handle_exceptions_are_collected(self, publisher: Publisher, subscriber1: Mock, subscriber2: Mock, subscribed_instance):
        subscriber1.side_effect = KeyError()
        result = publisher.handle(subscribed_instance)
        assert result == [subscriber1.side_effect, subscriber2.return_value]

