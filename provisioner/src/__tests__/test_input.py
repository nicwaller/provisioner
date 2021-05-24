from json.decoder import JSONDecodeError
from typing import List, cast

import pytest
from jsonschema.exceptions import ValidationError
from provisioner.src.core.input import parse

from provisioner.src.imperators.package import Package


def test_invalid_json():
    with pytest.raises(JSONDecodeError):
        parse("{")


def test_schema_failure():
    with pytest.raises(ValidationError):
        parse("{}")


def test_parse_package():
    steps = cast(List[Package], parse('[{"package":{"apache2":{"installed":true},"php":{"installed":true}}}]'))
    assert len(steps) == 2
    assert steps[0].key == "apache2"
    assert steps[0].installed == True
    assert steps[1].key == "php"
    assert steps[1].installed == True
