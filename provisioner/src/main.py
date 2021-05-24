import errno
import os
from datetime import datetime
from os import unlink
from typing import List


from imperators import BaseImperator, Observe
from logger import logger
from input import parse
from singleton import Singleton


def main():
    check_root()
    with Singleton():
        run()


def check_root():
    try:
        with open("/root/provisioner", "w") as file:
            file.write(datetime.today().strftime("%Y-%m-%d"))
        unlink("/root/provisioner")
    except IOError as e:
        if e.errno == errno.ENOENT:
            # /root doesn't exist? probably not on Linux.
            logger.critical("/root does not exist")
            logger.warning("This tool only works on Linux. Are you on a Mac?")
            raise RuntimeError("This cannot be run on a Mac") from None
        elif e.errno == errno.EPERM:
            logger.error("probably not running as root user")
            raise RuntimeError("this program must be run as root") from None
        else:
            pass


def run():
    steps: List[BaseImperator] = []
    with open(os.getenv('CONFIG_FILE', 'server.json'), "r") as file:
        steps.extend(parse(file.read()))

    # how to handle parent directories of files? least permission with traverse?


    # TODO: CLI to print out the current schema, or validate files against the built-in schema

    # Python's type checker can't quite handle this until >= 3.10
    # noinspection PyTypeChecker
    BaseImperator.add_listener(Observe.change_listener)

    for step in steps:
        step.apply()



    # TODO: emit a final status (did everything converge as expected? all the services running?)
