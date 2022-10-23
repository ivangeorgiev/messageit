import importlib
from logging import Logger, getLogger
import sys

class Command:
    executor: None
    logger: Logger = getLogger(__name__)

    def execute(self):
        if not self.executor:
            raise 
        return self.executor(self)

class LoadFileCommand(Command):
    def _execute(self, command):
        pass

    executor = _execute


class Event:
    observers = []
    logger: Logger = getLogger(__name__)

    def notify(self):
        for observe in self.observers:
            try:
                observe(self)
            except Exception as exception:
                self.logger.exception("Exception publishing event %s", self)


def main():
    for version in sys.argv[1:]:
        mod = importlib.import_module(f"{__package__}.{version}")
        mod.main()

main()
