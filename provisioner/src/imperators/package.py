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

    def apply(self, dryrun=False):

        if self.installed:
            if Package.is_installed(self.key):
                logger.debug(f"Package {self.key} is already installed")
                self.notify(False)
                return
            apt_verb = "install"
        else:
            if not Package.is_installed(self.key):
                logger.debug(f"Package {self.key} is already removed")
                self.notify(False)
                return
            apt_verb = "remove"
        command = ["apt-get", "-y", apt_verb, self.key]
        if dryrun:
            logger.info(f"[dryrun] would run command: {' '.join(command)}")
            self.notify(True)
        else:
            out = subprocess.run(command)
            if out.returncode != 0:
                logger.error("Something went wrong while manipulating packages")
            self.notify(True)

    @staticmethod
    def is_installed(name: str) -> bool:
        return (
            subprocess.run(
                ["dpkg", "-l", name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        ).returncode == 0
