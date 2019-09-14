# -*- coding: utf-8 -*-

from jwcrypto import jwk
from jwt_auth_client.client_manager import ClientManager


class TestClientManager(object):

    def test_client(self, get_s_token, get_key_set_fixture, mocker):
        jws_token = ClientManager(get_s_token)
        issuer = jws_token.get_issuer()
        assert issuer
        mocker.patch('jwt_auth_client.client_manager.ClientManager.'
                     '_get_serialized_key_set',
                     return_value=get_key_set_fixture)
        key_set = jws_token.get_key_set(issuer)
        assert isinstance(key_set, jwk.JWKSet)

        pub_key = jws_token.get_public_key(key_set)
        assert pub_key

        assert jws_token.verify_token(pub_key)
        assert jws_token.is_token_valid(key_set)

        # negative case for expired token
        import time
        time.sleep(5)
        jws_token = ClientManager(get_s_token)
        assert jws_token.verify_token(pub_key)
        assert jws_token.is_token_valid(key_set) == False
        assert 'Expired' in jws_token.message
