from __future__ import annotations


from typing import Dict, List, Set
import tempfile
import os
import shutil
import pwd
import grp
import logging
import subprocess

from .base import BaseImperator

logger = logging.getLogger("Observe")


class Observe(BaseImperator):
    resource_type: str = "observe"
    touched_resources: Set[str] = set()
    untouched_resources: Set[str] = set()

    def __init__(self, key: str, declaration: Dict):
        super().__init__(key, declaration)
        self.command: str = declaration["command"]

    def apply(self):
        if self.key in Observe.touched_resources:
            logger.info(f"Triggered observer {self.key}")
            out = subprocess.run(["bash", "-c", self.command])
            if out.returncode != 0:
                logger.error(
                    f"Something went wrong while running this observer {self.key}"
                )
        elif self.key in Observe.untouched_resources:
            logger.debug(f"Skipping observer for {self.key}")
        else:
            logger.warning(f"No matched resource for observer on {self.key}")
