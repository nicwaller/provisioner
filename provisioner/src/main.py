from typing import Set

from logger import logger
from datetime import datetime
from os import unlink
import errno
import json
from jsonschema import validate
import pkg_resources

# TODO: install with apt, or apt-get, or dpkg?
from imperators import BaseImperator, Package, FileCopy, Observe


def main():
    logger.info("starting up")

    try:
        with open("/root/provisioner", "w") as file:
            file.write(datetime.today().strftime('%Y-%m-%d'))
        unlink("/root/provisioner")
    except IOError as e:
        if e.errno == errno.ENOENT:
            # /root doesn't exist? probably not on Linux.
            logger.critical("/root does not exist")
            logger.info("This tool only works on Linux. Are you on a Mac?")
            return
        elif e.errno == errno.EPERM:
            logger.error("probably not running as root user")
        else:
            pass
            # print(e)

    # TODO: URL? env var?
    with open('server.json', 'r') as file:
        data = json.load(file)

    # how to handle parent directories of files? least permission with traverse?

    # remember to take backups of files

    # TODO: CLI to print out the current schema, or validate files against the built-in schema

    schema = json.loads(pkg_resources.resource_string(__name__, 'config.schema.json'))
    validate(data, schema)
    # TODO: log better error if schema validation fails

    # changed_resources: Set[str] = set()

    def listener(item: BaseImperator, changed: bool):
        if changed:
            Observe.touched_resources.add(f"{item.resource_type}[{item.key}]")
        else:
            Observe.untouched_resources.add(f"{item.resource_type}[{item.key}]")

    BaseImperator.add_listener(listener)

    resource_types = [Package, FileCopy, Observe]
    for stage in data:
        for imperator in resource_types:
            if imperator.resource_type in stage:
                packages = [imperator(key, declaration) for (key, declaration) in
                            stage[imperator.resource_type].items()]
                imperator.apply_multi(packages)


if __name__ == "__main__":
    try:
        main()
    finally:
        logger.info("exiting with status code 0")
