import logging
from typing import Dict, List, Callable

logger = logging.getLogger("BaseImperator")


class BaseImperator(object):
    resource_type: str = "base"
    changeListeners: List[Callable[[object, bool], None]] = []

    def __init__(self, key: str, declaration: Dict):
        self.key = key
        self.declaration = declaration

    def notify(self, changed=False):
        for listener in BaseImperator.changeListeners:
            listener(self, changed)

    @classmethod
    def apply_multi(cls, items: List[object]):
        for item in items:
            item.apply(False)

    """
    Implementors should call self.notify() from this method
    """

    def apply(self, dryrun=False):
        self.notify(False)
        raise NotImplemented

    # TODO: With Python >= 3.10 and __future__, type annotation can reference containing class
    @classmethod
    def add_listener(cls, fn: Callable[[object, bool], None]):
        cls.changeListeners.append(fn)
