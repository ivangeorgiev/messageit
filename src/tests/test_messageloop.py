import importlib
from typing import Any
from pytest_bdd import parsers, scenarios, given, when, then
from messageit._core import MessageLoop, DummyLogger
from messageit._protocols import LoggerProtocol, ResolverProtocol

scenarios("features/messageloop.feature")

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

@given("'FakeMessageLoop' instance with default arguments", target_fixture="messageloop")
def given_fakemessageloop_with_default_arguments():
    return FakeMessageLoop()

@given("'messageloop.running' bool attribute is set to 'True'")
def given_bool_atttribute_set(messageloop):
    setattr(messageloop, "running", bool("True"))

@when("'messageloop.stop()' is called")
def when_messageloop_stop_is_called(messageloop:FakeMessageLoop):
    messageloop.stop()

@when("MessageLoop instance is created with no arguments", target_fixture="messageloop")
def create_messageloop_without_logger():
    return FakeMessageLoop()

@then(parsers.parse("'{fixture_name}.{attribute_name}' attribute is set to '{expected_class}' instance"))
def should_have_attribute_instance(fixture_name, attribute_name, expected_class, request):
    instance = request.getfixturevalue(fixture_name)
    module_name,_,class_name = expected_class.rpartition(".")
    module = importlib.import_module(module_name)
    klass = getattr(module, class_name)
    assert isinstance(getattr(instance, attribute_name), klass)

@then(parsers.parse("'{fixture_name}.{attribute_name}' attribute is set to '{expected_value}'"))
def should_have_attribute_set(fixture_name, attribute_name, expected_value, request):
    instance = request.getfixturevalue(fixture_name)
    assert str(getattr(instance, attribute_name)) == expected_value
