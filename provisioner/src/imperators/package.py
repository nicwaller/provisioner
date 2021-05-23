from __future__ import annotations

from typing import Dict, List
import subprocess


class Package:
    key: str = "package"

    def __init__(self, declaration: Dict):
        # We can reasonably assume that the Package conforms to our JSON schema
        # Manual validation is only necessary for things not caught by the schema
        self.name = declaration['name']
        self.installed: bool = declaration['installed']

    @classmethod
    def apply(cls, items: List[Package]):
        installable = [x.name for x in items if x.installed]
        removable = [x.name for x in items if not x.installed]
        if len(installable) > 0:
            out = subprocess.run(["apt-get", "-y", "install", *installable])
        if len(removable) > 0:
            out = subprocess.run(["apt-get", "-y", "remove", *removable])
