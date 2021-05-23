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
            item.apply()

    """
    Implementors should call self.notify() from this method
    """

    def apply(self):
        self.notify(False)
        raise NotImplemented

    @classmethod
    def add_listener(cls, fn: Callable[[object, bool], None]):
        cls.changeListeners.append(fn)
