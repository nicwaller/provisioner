from __future__ import annotations

import logging
import subprocess
import sys
from typing import Dict, Set

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
            out = subprocess.run(["bash", "-c", self.command], capture_output=True)
            if out.returncode != 0:
                logger.error(
                    f"Something went wrong while running this observer {self.key}"
                )
                print(out.stdout)
                print(out.stderr, file=sys.stderr)
                # Being able to roll back a notifier resource would be interesting, but too much work
            else:
                logger.info(out.stdout.decode("utf-8").strip())
        elif self.key in Observe.untouched_resources:
            logger.debug(f"Skipping observer for {self.key}")
        else:
            logger.warning(f"No matched resource for observer on {self.key}")
