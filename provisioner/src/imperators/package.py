import logging
import re
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
            logger.info(f"Will install package: {self.key}")
            out = subprocess.run(command, stdout=subprocess.DEVNULL)
            if out.returncode != 0:
                logger.error("Something went wrong while manipulating packages")
            self.notify(True)

    @staticmethod
    def is_installed(name: str) -> bool:
        try:
            output = subprocess.check_output(["dpkg", "-l", name]).decode("utf-8")
            return re.search(f"ii\s*{name}", output) is not None
        except subprocess.CalledProcessError:
            # no matching packages
            return False

