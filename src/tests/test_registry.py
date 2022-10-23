from unittest.mock import Mock
import pytest

from messageit._registry import Registry, SimpleRegistry
from messageit import ANY_SUBJECT

class TestSimpleRegistryClass:
    @pytest.fixture(name="registry")
    def given_registry(self) -> SimpleRegistry:
        return SimpleRegistry()

    @pytest.fixture(name="subject")
    def given_subject(self):
        return "subject-123"

    @pytest.fixture(name="value1")
    def given_value1(self):
        return Mock()

    @pytest.fixture(name="value2")
    def given_value2(self):
        return Mock()

    def test_create_instance(self, registry):
        assert isinstance(registry, SimpleRegistry)
        assert isinstance(registry, Registry)

    def test_list_of_subjects_is_empty(self, registry):
        assert registry.subjects == []

    def test_assign_value_to_key(self, registry: Registry, subject, value1):
        result = registry.subscribe(subject, value1)
        assert result is registry, "returns self reference"
        assert subject in registry.subjects, "subject is added to subjects"
        assert list(registry.subscribers_of(subject)) == [value1], "value is added to the subject assigned values" 

    def test_duplicate_subject_assignment_is_ignored(self, registry: Registry, subject, value1):
        registry.subscribe(subject, value1)
        assert list(registry.subscribers_of(subject)) == [value1], "subscription is used only once" 

    def test_subscribers_to_any_subject_subscribe_to_all_subjects(self, registry: Registry, subject, value1 ):
        registry.subscribe(ANY_SUBJECT, value1)
        assert list(registry.subscribers_of(subject)) == [value1], "value is subscribed to any subject" 
