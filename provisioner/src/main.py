import errno
import os
import time
from datetime import datetime
from os import unlink
from typing import List

import click

from imperators import BaseImperator, Observe
from input import parse, print_schema
from logger import logger
from singleton import Singleton


@click.group()
def main():
    pass


# dry run


@click.command(help="Apply configuration on this server and exit")
@click.option("--dry-run", is_flag=True)
def run(dry_run: bool):
    check_root()
    with Singleton():
        perform(dry_run)


@click.command(help="Run as a daemon, periodically re-applying the configuration")
@click.option(
    "-i",
    "--interval",
    default=1800,
    help="Delay (in seconds) between runs",
    show_default=True,
    envvar="INTERVAL",
)
def daemon(interval: int):
    check_root()
    with Singleton():
        while True:
            perform(False)
            logger.info(f"Sleeping for {interval} seconds")
            time.sleep(interval)
            logger.info("Waking up")


@click.command(help="Display JSON schema for configuration")
def schema():
    print_schema()


main.add_command(run)
main.add_command(schema)
main.add_command(daemon)


# @click.command()
# @click.option("-s", "--schema")
# def main(schema):
#     if schema:
#         return
#


def check_root():
    try:
        with open("/root/provisioner", "w") as file:
            file.write(datetime.today().strftime("%Y-%m-%d"))
        unlink("/root/provisioner")
    except PermissionError:
        logger.error("probably not running as root user")
        raise RuntimeError("this program must be run as root") from None
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
            raise NotImplementedError()


def perform(dryrun=False):
    steps: List[BaseImperator] = []
    with open(os.getenv("CONFIG_FILE", "server.json"), "r") as file:
        steps.extend(parse(file.read()))

    # how to handle parent directories of files? least permission with traverse?

    # TODO: CLI to print out the current schema, or validate files against the built-in schema

    # Python's type checker can't quite handle this until >= 3.10
    # noinspection PyTypeChecker
    BaseImperator.add_listener(Observe.change_listener)

    for step in steps:
        step.apply(dryrun=False)

    # TODO: emit a final status (did everything converge as expected? all the services running?)
