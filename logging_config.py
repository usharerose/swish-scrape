# Copyright (c) 2021 usharerose. All rights reserved.
from logging.config import dictConfig


DEFAULT_LOG_CONFIG_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': ('%(asctime)s | %(process)d | %(levelname)s | +%(lineno)d %(name)s '
                       '|> %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'plain': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        '': {
            'handlers': ['plain'],
            'level': 'INFO',
        },
    },
}


def config_logging():
    dictConfig(DEFAULT_LOG_CONFIG_DICT)
