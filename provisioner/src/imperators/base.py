from __future__ import annotations

from typing import Dict, List, Callable
import logging

logger = logging.getLogger('BaseImperator')



class BaseImperator:
    resource_type: str = "base"
    changeListeners: List[Callable[[BaseImperator, bool], None]] = []

    def __init__(self, key: str, declaration: Dict):
        self.key = key
        self.declaration = declaration

    def notify(self, changed=False):
        for listener in BaseImperator.changeListeners:
            listener(self, changed)

    @classmethod
    def apply_multi(cls, items: List[BaseImperator]):
        for item in items:
            item.apply()

    """
    Implementors should call self.notify() from this method
    """

    def apply(self):
        self.notify(False)
        raise NotImplemented

    @classmethod
    def add_listener(cls, fn: Callable[[BaseImperator, bool], None]):
        cls.changeListeners.append(fn)
