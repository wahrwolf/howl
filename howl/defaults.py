from logging import DEBUG

logger_config = {
    "version" : 1,
    "formatters" : {
        'brief': {'format': '%(name)-8s %(message)s'}
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
