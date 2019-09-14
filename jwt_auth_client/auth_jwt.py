# -*- coding: utf-8 -*-
"""auth_jwt for endpoints"""

import logging

from functools import wraps
from flask import request
from .exceptions import Unauthorized, BadRequest

from .client_manager import ClientManager


def get_auth(token):
    """Return dictionary with identity in case tiken is valid;
    otherwise return False
    """
    jwt_manager = ClientManager(token)
    if jwt_manager.message:
        raise BadRequest(jwt_manager.message)   # pragma: no cover
    issuer = jwt_manager.get_issuer()
    key_set = jwt_manager.get_key_set(issuer)
    pub_key = jwt_manager.get_public_key(key_set)
    if jwt_manager.is_token_valid(key_set) and\
            jwt_manager.verify_token(pub_key):
        return jwt_manager.claims
    raise Unauthorized(jwt_manager.message)


def check_auth(token):
    """Check whether username and password fit"""
    jwt_manager = ClientManager(token)
    if jwt_manager.message:
        return False, jwt_manager.message
    issuer = jwt_manager.get_issuer()
    key_set = jwt_manager.get_key_set(issuer)
    pub_key = jwt_manager.get_public_key(key_set)
    if jwt_manager.is_token_valid(key_set) and\
            jwt_manager.verify_token(pub_key):
        return True, None
    return False, jwt_manager.message   # pragma: no cover


def requires_auth_jwt(f):
    """Decorate with this method an endpoint in order to add jwt_auth"""
    @wraps(f)
    def decorated(*args, **kwargs):
        logger = logging.getLogger()
        logger.debug({'auth': request.authorization})
        token = None
        if request.headers.get('Authorization'):
            auth = request.headers.get('Authorization')
            if len(auth.split()) == 2:
                token = auth.split()[1]
        if not token:
            raise BadRequest('Please provide valid JSON web token')
        status, message = check_auth(token)
        if not status:
            raise Unauthorized(str(message))
        return f(*args, **kwargs)
    return decorated
