"""Provide defaults as well as getter for the howl project
"""

from logging import DEBUG
from os import environ

LOGGER_CONFIG = {
    "version" : 1,
    "formatters" : {
        'brief': {'format': '[%(levelname)s]: %(message)s'}
    }, "handlers" : {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief',
            'level': DEBUG}
    }, "root" : {
        'handlers': ['console'],
        'level': DEBUG,
    }
}

RUNTIME_OPTIONS = {
        "editor" : {
            "encoding" : "utf-8",
            "path" : environ.get("EDITOR", "vi")
            }
        }
