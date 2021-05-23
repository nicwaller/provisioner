from __future__ import annotations

import logging
import subprocess
from typing import Dict

from .base import BaseImperator

logger = logging.getLogger("Package")


class Package(BaseImperator):
    resource_type: str = "package"

    def __init__(self, key: str, declaration: Dict):
        super().__init__(key, declaration)
        self.installed: bool = declaration["installed"]

    def apply(self):
        if Package.is_installed(self.key):
            logger.debug(f"Package {self.key} is already installed")
            self.notify(False)
            return

        if self.installed:
            apt_verb = "install"
        else:
            apt_verb = "remove"
        out = subprocess.run(["apt-get", "-y", apt_verb, self.key])
        if out.returncode != 0:
            logger.error("Something went wrong while manipulating packages")
        self.notify(True)

    @staticmethod
    def is_installed(name: str) -> bool:
        return (
            subprocess.run(["dpkg", "-l", name], stdout=subprocess.DEVNULL)
        ).returncode == 0

    # PERF: we could use apply_multi() to install several packages at once, but the feedback is more complex
    # @classmethod
    # def apply_multi(cls, items: List[Package]):
    #     # Want to detect what changes we made? could parse `apt -qq list apache2 foo php`
    #     for x in items:
    #         x.notify(True)  # FIXME: only notify when installed
    #     installable = [x.key for x in items if x.installed]
    #     removable = [x.key for x in items if not x.installed]
    #     if len(installable) > 0:
    #         out = subprocess.run(["apt-get", "-y", "install", *installable])
    #         if out.returncode != 0:
    #             logger.error('Something went wrong while installing packages')
    #     if len(removable) > 0:
    #         out = subprocess.run(["apt-get", "-y", "remove", *removable])
    #         if out.returncode != 0:
    #             logger.error('Something went wrong while removing packages')
