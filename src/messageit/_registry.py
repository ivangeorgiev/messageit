
from abc import ABC, abstractmethod
from typing import Any, DefaultDict, Hashable, List

class ANY_SUBJECT:
    """Subscribes to this subject are subscribed to all subjects."""
    ...

class Registry(ABC):
    """Maintain subscribers with subjects"""

    @property
    def subjects(self):
        return self.get_subjects()

    @abstractmethod
    def get_subjects(self) -> List:
        """Get list of subjects"""

    @abstractmethod
    def subscribe(self, subject: Hashable, value: Any) -> 'Registry':
        """Append value to subject assignment"""

    @abstractmethod
    def subscribers_of(self, subject: Hashable) -> List:
        """Get list of values assigned with a subject"""

class Validator(ABC):
    """Validate assignments"""
    @abstractmethod
    def __call__(self, registry: Registry, subject: Hashable, value: Any) -> bool:
        """Validate assginment"""

class AlwaysValid(Validator):
    """Always valid"""
    def __call__(self, registry: Registry, subject: Hashable, value: Any) -> bool:
        return True

class AllValid(Validator):
    """Valid if all rules are valid"""
    _validators: List[Validator]

    def __init__(self, rules: List[Validator]):
        self._rules = rules.copy()

    def __call__(self, registry: Registry, subject: Hashable, value: Any) -> bool:
        for validator in self._validators:
            if not validator(registry, subject, value):
                return False
        return True

class AnyValid(Validator):
    """Valid if at least one rule is valid"""
    _validators: List[Validator]

    def __init__(self, rules: List[Validator]):
        self._rules = rules.copy()

    def __call__(self, registry: Registry, subject: Hashable, value: Any) -> bool:
        for validator in self._validators:
            if validator(registry, subject, value):
                return True
        return False


class SimpleRegistry(Registry):
    _subscriptions: DefaultDict
    _validator: Validator

    def __init__(self) -> None:
        self._subscriptions = DefaultDict(list)
        self._validator = AlwaysValid()

    def subscribers_of(self, subject: Hashable) -> List:
        return set(self._subscriptions[ANY_SUBJECT] + self._subscriptions[subject])

    def get_subjects(self) -> List:
        return list(self._subscriptions.keys())

    def subscribe(self, subject: Hashable, value: Any) -> 'Registry':
        if self._validator(self, subject, value):
            self._subscriptions[subject].append(value)
        return self

