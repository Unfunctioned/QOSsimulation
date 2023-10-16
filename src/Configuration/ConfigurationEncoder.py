import json
from typing import Any
from Configuration.BaseConfig import BaseConfig
from random import Random
'''JSON encoder for simulation configurations'''
class ConfigurationEncoder(json.JSONEncoder):
    
    def default(self, o: object) -> Any:
        if isinstance(o, BaseConfig):
            return o.jsonable()
        return json.JSONEncoder.default(self, o)