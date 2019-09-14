# -*- coding: utf-8 -*-
"""in order to redefine variables from core.config
make it in core.lcoal_config
"""

import os
import yaml
from .config import BaseConfig
from .pattern_solution import singleton


@singleton
class Config(BaseConfig):
    """BasecConfig child where project params can be
    redefined
    """

    def __init__(self):
        """Init params"""
        locations = ["pn_service.yaml",
                     "/etc/webapps/jwt_auth_client.yaml"]
        if "CONFIG" in os.environ:
            locations = [os.environ["CONFIG"]]

        for path in locations:
            if not os.path.exists(path):
                continue
            config = yaml.load(open(path))

            config["config_file_name"] = path
            config["version"] = 1

            self.__dict__.update(config)
            break
        else:
            raise SystemExit("no YAML config file found")
