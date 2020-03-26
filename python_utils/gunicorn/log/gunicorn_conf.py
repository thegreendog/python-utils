"""Gunicorn specific settings"""
import sys

from python_utils.gunicorn.log.formatters import GunicornRequestGELFFormatter
from python_utils.gunicorn.log.loggers import GunicornLogger

logger_class = GunicornLogger
worker_class = 'gthread'
accesslog = '-'
workers = 1
worker_connections = 1000

LOG_LEVEL = 'INFO'
loglevel = LOG_LEVEL.lower()

logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'request_gelf': {
            '()': GunicornRequestGELFFormatter
        }
    },
    'root': {
        'handlers': ['server_request'],
        'level': 'WARNING',
    },
    'handlers': {
        'server_request': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'request_gelf',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'gunicorn.error': {
            'handlers': ['server_request'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['server_request'],
            'level': LOG_LEVEL,
            'propagate': False,
        }
    }
}
