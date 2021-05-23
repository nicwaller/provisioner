from __future__ import annotations

import grp
import logging
import os
import pwd
import shutil
import tempfile
from typing import Dict

from .base import BaseImperator

logger = logging.getLogger("FileCopy")


class FileCopy(BaseImperator):
    resource_type: str = "file_copy"

    def __init__(self, key: str, declaration: Dict):
        super().__init__(key, declaration)
        self.source: str = declaration["source"]
        self.mode: str = declaration["mode"]
        self.owner: str = declaration["owner"]
        self.group: str = declaration["group"]

    def apply(self):
        # Be careful about avoiding temporary race conditions... use hard linking to move into place? Does move preserve permissions?
        # Yes, moving a file does preserve mode, etc. that will work.
        # How to support large file copies?

        logger.debug("doing a file")
        # prepare a temporary copy
        tmpFilePath = tempfile.mktemp()
        shutil.copy(self.source, tmpFilePath)
        # Get everything ready
        # FIXME: handle missing modes
        os.chmod(tmpFilePath, int(self.mode, base=8))
        uid = pwd.getpwnam(self.owner).pw_uid
        gid = grp.getgrnam(self.group).gr_gid
        os.chown(tmpFilePath, uid, gid)
        # Once it's fully ready, move it into place
        os.rename(tmpFilePath, self.key)
        logger.info(f"Created {self.key}")
        self.notify(True)
