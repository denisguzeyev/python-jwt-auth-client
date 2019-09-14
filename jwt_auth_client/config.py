# -*- coding: utf-8 -*-
"""base project configuration"""


from pythonjsonlogger import jsonlogger


class BaseConfig(object):
    """Base config class with params:
    can be redefined in core.local_config
    """

    DEBUG = False
    DEVELOPMENT = True
    CSRF_ENABLED = True
    DATABASE_URI = ''

    ECHO = False
    LOGGER_STATUS_CODE = [200, 300, 400, 500]

    AUTH_ADMIN_PASSWORD = None

    JWT_CONF_YAML_PATH = 'jwt_conf.yaml'

#     APPLICATION_ROOT = '/'
    LOGGING_CONF = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                '()': jsonlogger.JsonFormatter,
                'fmt': '%(asctime)s %(msecs)s\
                    %(levelname)s %(lineno)d %(funcName)s %(message)s\
                    %(filename) %(module)s %(pathname)s %(relativeCreated)s\
                    %(process)d %(processName)s\
                    %(thread)s %(threadName)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'info_file_handler': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/jwt_auth_client.log',
                # "maxBytes": 500000000,
                "encoding": "utf8",
                # "backupCount": 10000,
                "backupCount": 10,
                "when": "midnight",
                "interval": 1
            },
            'error_file_handler': {
                'level': 'ERROR',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/jwt_auth_client_error.log',
                "encoding": "utf8",
                "backupCount": 10,
                "when": "midnight",
                "interval": 1
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'info_file_handler'],
                'level': 'DEBUG',
            },
            'error': {
                'handlers': ['error_file_handler'],
                'level': 'ERROR',
            },
            'alembic': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }
