# -*- coding: utf-8 -*-
"""jwt server part"""

import time
import datetime

from jwcrypto import jwt, jwk


class ServerManager(object):
    """Access tokens JWT() producer and key_set JWKSet() supplier
    This class has been added to "client" part only for test purposes
    """

    def get_private_cert(self):
        """Return private RSA certificate"""
        return str.encode(open('certificates/jwt/private.pem').read())

    def get_public_cert(self):
        """Return public RSA certificate"""
        return str.encode(open('certificates/jwt/public.pem').read())

    def get_key_set(self):
        """Return key_set (JWKSet) that includes only public key(s)"""
        public_cert = self.get_public_cert()
        key_set = jwk.JWKSet()
        public_key = jwk.JWK()
        public_key.import_from_pem(public_cert)
        key_set.add(public_key)
        return key_set

    def get_signed_token(self, be_valid=30, leeway=0):
        """Return signed JWT (not serialized)
        be_valid by default is set to 30 seconds
        """
        now = datetime.datetime.now()
        now_timestamp = time.time()
        now_plus = now + datetime.timedelta(seconds=be_valid)
        now_plus_timestamp = time.mktime(now_plus.timetuple())
        private_cert = self.get_private_cert()
        private_key = jwk.JWK()
        private_key.import_from_pem(private_cert)
        token = jwt.JWT(header={"alg": "RS256",
                                "typ": "JWT",
                                "kid": private_key.key_id},
                        claims={"info": "I'm a signed token",
                                "iss": "zebra_numa",
                                "nbf": now_timestamp,
                                "exp": now_plus_timestamp,
                                "leeway": leeway
                                }
                        )
        token.make_signed_token(private_key)
        return token
