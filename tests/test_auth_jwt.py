# -*- coding: utf-8 -*-

import time
import pytest
from flask import url_for
from jwt_auth_client.auth_jwt import check_auth, get_auth
from jwt_auth_client.exceptions import Unauthorized


def test_auth_jwt(mocker, get_key_set_fixture, get_s_token):
    mocker.patch('jwt_auth_client.client_manager.ClientManager.'
                 '_get_serialized_key_set',
                 return_value=get_key_set_fixture)
    assert check_auth(get_s_token)


def test_get_auth_jwt(mocker, get_key_set_fixture, get_s_token):
    mocker.patch('jwt_auth_client.client_manager.ClientManager.'
                 '_get_serialized_key_set',
                 return_value=get_key_set_fixture)
    assert get_auth(get_s_token)
    assert isinstance(get_auth(get_s_token), dict)
    # negative case with expired token
    time.sleep(3)
    with pytest.raises(Unauthorized):
        assert get_auth(get_s_token)


def test_requires_auth_jwt(mocker, client, get_key_set_fixture,
                           get_auth_headers, get_empty_auth_headers,
                           get_auth_basic_headers):
        mocker.patch('jwt_auth_client.client_manager.ClientManager.'
                     '_get_serialized_key_set',
                     return_value=get_key_set_fixture)
        res_endpoint = client.\
                        get((url_for('protected')),
                            headers=get_auth_headers,
                             content_type='multipart/form-data')
        assert res_endpoint.headers['Content-Type'] == 'application/json'
        assert res_endpoint.status_code == 200
        assert 'accepted' in str(res_endpoint.data)

        # negative case for invalid (empty) token
        res_endpoint = client.\
                        get((url_for('protected')),
                            headers=get_empty_auth_headers,
                             content_type='multipart/form-data')
        assert res_endpoint.headers['Content-Type'] == 'application/json'
        assert res_endpoint.status_code == 400
        assert 'Please provide valid JSON web token' in str(res_endpoint.data)

        # negative case for invalid token
        res_endpoint = client.\
                        get((url_for('protected')),
                            headers=get_auth_basic_headers,
                             content_type='multipart/form-data')
        assert res_endpoint.headers['Content-Type'] == 'application/json'
        assert res_endpoint.status_code == 401
        assert 'Invalid JWS Object' in str(res_endpoint.data)
