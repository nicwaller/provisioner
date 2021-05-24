import logging
import os
import sys
from datetime import datetime

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT)
# d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        log_record['level'] = record.levelname


rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

if os.getenv('LOG', 'plain') == 'JSON':
    jsonHandler = logging.StreamHandler()
    jsonHandler.setFormatter(CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s'))
    rootLogger.addHandler(jsonHandler)
else:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    rootLogger.addHandler(handler)


logger = rootLogger.getChild("provisioner")
logger.debug("Logger is ready")

# logger.warning('Protocol problem: %s', 'connection reset', extra=d)

