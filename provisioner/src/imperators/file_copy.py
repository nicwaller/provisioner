from __future__ import annotations

import grp
import logging
import os
import pwd
import shutil
import tempfile
from typing import Dict
import subprocess

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
        try:
            self.conflict: str = declaration["conflict"]
        except KeyError:
            self.conflict: str = "backup"
        try:
            self.action: str = declaration["action"]
        except KeyError:
            self.action: str = "create"
        # TODO: I need a way to delete index.html so that index.php can shine through

    def apply(self):
        # Be careful about avoiding temporary race conditions... use hard linking to move into place? Does move preserve permissions?
        # Yes, moving a file does preserve mode, etc. that will work.
        # How to support large file copies?

        if self.action == "delete":
            try:
                os.unlink(self.key)
                logger.info(f"Deleted file {self.key}")
                # TODO: maybe backup here too
                self.notify(True)
            except FileNotFoundError:
                logger.debug(f"No file to delete at {self.key}")
                self.notify(False)
            return

        if os.path.isdir(self.key):
            logger.warning(f"Desired file ${self.key} already exists as directory")
            self.notify(False)
            return
        elif os.path.islink(self.key):
            logger.warning(f"Desired file ${self.key} already exists as link")
            self.notify(False)
            return
        elif os.path.isfile(self.key):
            original_hash = FileCopy.sha_256_sum(self.key)
            desired_hash = FileCopy.sha_256_sum(self.source)
            # TODO: maybe show a diff? or before/after byte sizes?
            if original_hash == desired_hash:
                logger.debug("Files are already identical")  # FIXME: Content may be, but what about the metadata?
                self.notify(False)
            else:
                if self.conflict == "abort":
                    logger.warning(f"Aborting change to ${self.key} due to specified conflict behaviour")
                    self.notify(False)
                    return
                elif self.conflict == "backup":
                    raise NotImplementedError("FileCopy conflict behaviour: backup")  # TODO: do this
                elif self.conflict == "overwrite":
                    self.copy_into_place()
                    self.notify(True)
                else:
                    raise NotImplementedError
        elif not os.path.exists(self.key):
            self.copy_into_place()
            self.notify(True)
        else:
            raise NotImplementedError

        # if the same, do nothing. just pass.

        # if non-existent, do the normal.

        # if exists, and if conflict, follow the requested conflict behaviour.

    @staticmethod
    def sha_256_sum(path: str) -> str:
        proc = subprocess.run(["shasum", "-a256", path], capture_output=True)
        return proc.stdout.decode("utf-8").split(" ")[0]

    #     ubuntu@ip-10-193-71-185:/tmp/kitchen/data$ shasum -a256 apache2_restarted | awk '{print $1}'
    # 961198931557c09f72eb92e8acbee0dd279d4858be322a7ebb7b31564d8e3f5b

    def copy_into_place(self):
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
