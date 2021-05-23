from logger import logger
from datetime import datetime
from os import unlink
import errno
import json
from jsonschema import validate
import pkg_resources

# TODO: install with apt, or apt-get, or dpkg?
from imperators.package import Package
from imperators.file_copy import FileCopy


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

    for stage in data:
        for imperator in [Package, FileCopy]:
            if imperator.key in stage:
                packages = [imperator(declaration) for declaration in stage[imperator.key]]
                imperator.apply(packages)
        # if 'package' in stage:
        #     packages = [Package(declaration) for declaration in stage['package']]
        #     Package.apply(packages)
        # if 'file_copy' in stage:
        #     files = [FileCopy(declaration) for declaration in stage['file_copy']]
        #     FileCopy.apply(files)

    # logger.info("will install apache2")
    # list_files = subprocess.run(["apt-get", "-y", "install", "apache2", "php"])
    # print("The exit code was: %d" % list_files.returncode)

    with open("/var/www/html/index.php", "w") as file:
        # TODO: keep a copy
        # TODO: compare hashes to identify differences and log info
        file.truncate(0)
        file.write(
            """
    <?php
    header("Content-Type: text/plain");
    echo "Hello, world!\\n";
    """.lstrip()
        )


if __name__ == "__main__":
    try:
        main()
    finally:
        logger.info("exiting with status code 0")

