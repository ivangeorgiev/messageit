from typing import DefaultDict
import pytest

"""
- Registry is a dictionary
- You supply item factory used to create missing items

- Add dictionary access
"""

# class Registry:
#     items

class IgnoreDuplicatesValidator:
    ...

class FailOnDuplicateSubscription:
    def __call__(self, subscribers, new_subscriber) -> bool:
        if new_subscriber in subscribers:
            raise ValueError("Already subscribed for the topic")
        return True


class SubscriptionManager:
    _topics: DefaultDict
    _validators: list

    def __init__(self, validators: list = None):
        self._topics = DefaultDict(list)
        self._validators = list(validators or [])

    @property
    def topics(self):
        """Returns a list of topics with subscribers"""
        return self._topics.keys()

    def subscribers_of(self, topic):
        """Get subscribers for a topic"""
        if topic in self._topics:
            return tuple(self._topics[topic])
        return ()

    def subscribe(self, topic, subscriber):
        subscribers = self.subscribers_of(topic)
        for validate in self._validators:
            if not validate(subscribers, subscriber):
                return
        self._topics[topic].append(subscriber)

    def __setitem__(self, topic, subscriber):
        self.subscribe(topic, subscriber)

    def __getitem__(self, topic):
        return self.subscribers_of(topic)


class TestSubscriber:
    @pytest.fixture(name="subscription_manager")
    def given_subscribtion_manager(self):
        return SubscriptionManager()

    def test_list_of_topics_is_empty(self, subscription_manager):
        assert len(subscription_manager.topics) == 0

    def test_can_get_list_of_subscribers_for_a_topic(self, subscription_manager):
        subscription_manager.subscribers_of("topic")

    def test_can_subscribe(self, subscription_manager):
        subscription_manager.subscribe("topic", "subscriber")
        assert "topic" in subscription_manager.topics
        assert (len(subscription_manager.subscribers_of("topic"))) == 1
        assert "subscriber" in subscription_manager.subscribers_of("topic")

    def test_can_access_topic_as_dictionary(self, subscription_manager):
        subscription_manager.subscribe("topic", "subscriber")
        assert subscription_manager["topic"] == ("subscriber",)

    def test_setting_a_topic_as_dictionary_item_adds_subscription(
        self, subscription_manager
    ):
        subscription_manager["topic"] = "subscriber"
        assert subscription_manager["topic"] == ("subscriber",)

    def test_can_subscribe_multiple_times_for_same_topic(self, subscription_manager):
        subscription_manager["topic"] = "subscriber"
        subscription_manager["topic"] = "subscriber"
        assert subscription_manager["topic"] == (
            "subscriber",
            "subscriber",
        )

    def test_can_subscribe_only_once_times_for_same_topic(self):
        subscription_manager = SubscriptionManager(validators=[FailOnDuplicateSubscription()])
        subscription_manager["topic"] = "subscriber"
        with pytest.raises(ValueError):
            subscription_manager["topic"] = "subscriber"
        assert subscription_manager["topic"] == ("subscriber",)
