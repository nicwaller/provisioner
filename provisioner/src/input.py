import json
import logging
from typing import List

import pkg_resources
from jsonschema import validate

from imperators import BaseImperator
from imperators import Package, File, Observe

schema = json.loads(pkg_resources.resource_string(__name__, "config.schema.json"))

logger = logging.getLogger("Input")


def parse(userdata: str) -> List[BaseImperator]:
    try:
        data = json.loads(userdata)
    except json.decoder.JSONDecodeError as e:
        logger.critical("Input is not valid JSON")
        raise e
    try:
        validate(data, schema)
    except BaseException as e:
        logger.critical("got something")
        raise e

    all_items: List[BaseImperator] = []
    resource_types = [Package, File, Observe]
    for stage in data:
        for imperator in resource_types:
            if imperator.resource_type in stage:
                all_items.extend([
                    imperator(key, declaration)
                    for (key, declaration) in stage[imperator.resource_type].items()
                ])
    return all_items
