# -*- coding: utf-8 -*-
"""application's reginstration is here"""

from flask import Flask
from flask_restful import Resource, Api

from .local_config import Config
from jwt_auth_client.auth_jwt import requires_auth_jwt

config = Config()

flask_project = Flask(__name__)
flask_project.config.from_object(config)


api = Api(catch_all_404s=True, prefix='/root')


class Protected(Resource):
    """Entry point: protected (for test purposes)"""

    @requires_auth_jwt
    def get(self):
        """Return accepted 200 or unauthorized depends on provided
        Bearer token in Authorization header
        """
        return {'message': 'accepted'}, 200


api.add_resource(Protected, '/protected/', endpoint='protected')
api.init_app(flask_project)
