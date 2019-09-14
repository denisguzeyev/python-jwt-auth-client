# -*- coding: utf-8 -*-

import os
import json
import pytest
import pytz
from io import StringIO, BytesIO
import random
import base64

PROJECT_ROOT = os.path.dirname(__file__)

# Override test config before importing any local modules
os.environ["CONFIG"] = os.path.join(PROJECT_ROOT, "test.yaml")

from jwt_auth_client.local_config import Config
from jwt_auth_client.bunch import Bunch
from jwt_auth_client.server_manager import ServerManager
from jwt_auth_client.flask_project import flask_project


@pytest.fixture(scope='session')
def app():
    return flask_project


@pytest.fixture()
def get_s_token():
    server_manager = ServerManager()
    token = server_manager.get_signed_token(be_valid=2)
    return token.serialize()


@pytest.fixture()
def get_key_set_fixture():
    server_manager = ServerManager()
    key_set = server_manager.get_key_set()
    return key_set.export()


@pytest.fixture()
def get_auth_headers(get_s_token):
    return {"Authorization": "Bearer {}".format(get_s_token)}


@pytest.fixture()
def get_empty_auth_headers():
    return {"Authorization": "Bearer {}".format('')}


@pytest.fixture()
def get_auth_basic_headers():
    return {"Authorization": "Basic {user}".\
            format(user=base64.b64encode('admin:admin'.encode()).decode())}
