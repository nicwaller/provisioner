"""
It would be bad to have two provisioners running at once on the same system.
So let's try to be sure we're the only one around.
"""
import logging
import os

logger = logging.getLogger("Singleton")


class Singleton(object):
    pidfile = "/var/run/provisioner.pid"

    def __enter__(self):
        logger.info("Starting up...")
        if os.path.exists(self.pidfile):
            with open(self.pidfile, "r+") as file:
                other_pid = int(file.read())
                if pid_exists(other_pid):
                    logger.critical(
                        f"Another provisioner is already running! pid={other_pid}"
                    )
                    raise RuntimeError("Duplicate process") from None
                else:
                    logger.warning(f"Removing stale pidfile")
                    file.truncate()
                    file.write(str(os.getpid()))
        else:
            with open(self.pidfile, "w") as file:
                file.write(str(os.getpid()))
                logger.debug("Wrote pidfile.")
            logger.debug("No conflicting processes found.")

    # noinspection PyShadowingBuiltins
    def __exit__(self, _, value, traceback):
        os.unlink(self.pidfile)
        logger.info("Done")  # TODO: log the time spent, and maybe update metrics


def pid_exists(pid) -> bool:
    """
    Check For the existence of a unix pid.
    https://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid-in-python
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
