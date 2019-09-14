# -*- coding: utf-8 -*-
"""jwt client part"""

import json

import requests
import yaml
from jwcrypto import jwt, jwk, jws

from repoze.lru import lru_cache, ExpiringLRUCache

from .local_config import Config

cache = ExpiringLRUCache(3, 60 * 60 * 12)


class ClientManager(object):
    """Verification and deserialization of provided token"""

    def __init__(self, token):
        """Init params: create JWS() instance in order to deserilize
        provided 'raw' token
        """
        self.raw_token = token
        self.jwstoken = jws.JWS()
        self.message = None
        self.claims = None
        try:
            self.jwstoken.deserialize(self.raw_token)
        except jws.InvalidJWSObject as e:   # pragma: no cover
            self.message = e

    def get_issuer(self):
        """Return issuer of provided token"""
        return json.loads(self.jwstoken.objects.get('payload').
                          decode('utf-8')).get('iss')

    @lru_cache(3, cache=cache)
    def _get_serialized_key_set(self, issuer):  # pragma: no cover
        """Return serialized token n JSON format"""
        config = Config()
        jwt_conf_yaml = yaml.load(open(config.JWT_CONF_YAML_PATH))
        if not jwt_conf_yaml:
            raise Exception('JWT_CONF_YAML_PATH was not set in config file!')
        response = requests.get(jwt_conf_yaml.get(issuer))
        return response.content

    def get_key_set(self, issuer):
        """Return JWKSet (that has dict type)"""
        serialized_key_set = self._get_serialized_key_set(issuer)
        return jwk.JWKSet().from_json(serialized_key_set)

    def get_public_key(self, key_set):
        """Return public key that corresponds to delivered token"""
        key_id = (json.loads(self.jwstoken.objects.get('protected')).
                  get('kid'))
        return key_set.get_key(key_id)

    def verify_token(self, pub_key):
        """Return True if token properly signed;
        otherwise return False
        """
        self.jwstoken.verify(pub_key)
        return self.jwstoken.is_valid

    def is_token_valid(self, key_set):
        """Check whether provided token is valid
        (checking for expiration is built-in jwttoken.deserialize())
        """
        jwttoken = jwt.JWT()
        try:
            if str(json.loads(self.jwstoken.objects.get('payload').
                              decode('utf-8')).get('leeway')):
                jwttoken.leeway = json.loads(self.jwstoken.objects.
                                             get('payload').decode('utf-8')).\
                                             get('leeway')
            jwttoken.deserialize(jwt=self.raw_token, key=key_set)
            self.claims = json.loads(jwttoken.claims)
            return True
        except jwt.JWTExpired as e:
            self.message = str(e)
            return False
        self.message = 'Wrong token'    # pragma: no cover
        return False    # pragma: no cover
