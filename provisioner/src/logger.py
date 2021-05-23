import sys
import logging

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT)
# d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
rootLogger.addHandler(handler)

logger = rootLogger.getChild("provisioner")
logger.debug("Logger is ready")

# logger.warning('Protocol problem: %s', 'connection reset', extra=d)
