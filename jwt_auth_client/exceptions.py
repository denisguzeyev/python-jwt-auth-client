# -*- coding: utf-8 -*-
"""custom project exceptions"""

from flask_restful import HTTPException


class BadRequest(HTTPException):
    """Provide custom 400 exception"""

    code = 400
    pass


class Unauthorized(HTTPException):
    """Provide custom 401 exception"""

    code = 401
    pass
