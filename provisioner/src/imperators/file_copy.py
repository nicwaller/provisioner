from __future__ import annotations


from typing import Dict, List
import tempfile
import os
import shutil
import pwd
import grp
import logging

logger = logging.getLogger('FileCopy')


class FileCopy:
    key: str = "file_copy"

    def __init__(self, declaration: Dict):
        # We can reasonably assume that the Package conforms to our JSON schema
        # Manual validation is only necessary for things not caught by the schema
        self.destination: str = declaration['destination']
        self.source: str = declaration['source']
        self.mode: str = declaration['mode']
        self.owner: str = declaration['owner']
        self.group: str = declaration['group']

    @classmethod
    def apply(cls, items: List[FileCopy]):
        # Be careful about avoiding temporary race conditions... use hard linking to move into place? Does move preserve permissions?
        # Yes, moving a file does preserve mode, etc. that will work.
        # How to support large file copies?

        for item in items:
            logger.debug("doing a file")
            # prepare a temporary copy
            tmpFilePath = tempfile.mktemp()
            shutil.copy(item.source, tmpFilePath)
            # Get everything ready
            os.chmod(tmpFilePath, int(item.mode, base=8))
            uid = pwd.getpwnam(item.owner).pw_uid
            gid = grp.getgrnam(item.group).gr_gid
            os.chown(tmpFilePath, uid, gid)
            # Once it's fully ready, move it into place
            os.rename(tmpFilePath, item.destination)
            logger.info(f"Created ${item.destination}")
