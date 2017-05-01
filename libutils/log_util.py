#! /usr/bin/env python
"""
    Logger Utility

    Set ups logger to 'newtonsystems' style

    Usage:
        from libutils import log_util

        log_util.get_logger(__name__)
"""
import logging
import logging.config
import os
import sys

import libutils


DEV_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s,%(msecs)03d %(levelname)-8s %(name)s  %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S',
        },
        'colored': {
            '()': 'libutils.log_formatters.LevelFormatter',
            #'format': '%(log_color)s%(asctime)s %(levelname)-8s %(name)s  %(message)s',
            'log_colors' : {
                'DEBUG':    'grey',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'purple',
            }
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'colored',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'libutils.handlers.GenRotatingFileHandler',
            'base_filename': os.path.join(
                os.environ.get('LOG_DIR', '.'),
                os.environ.get('BASE_LOG_FILE', 'app'),
            ),
            'suffix_filename': 'log',
            'when': 'h',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': 'DEBUG',
        },
        'pika': {
            'level': 'INFO',
        },
        'iso8601.iso8601': {
            'level': 'INFO',
        },
        'rabbitmq.exchange.monitor.fanout': {
            'level': 'WARNING',
        },
    }
}


PROD_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s,%(msecs)03d %(levelname)-8s %(name)s  %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S',
        },
        'logstash': {
            '()' : 'libutil.log_formatters.LogstashFormatter',
        },
    },
    'handlers': {
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'libutil.handlers.GenRotatingFileHandler',
            'base_filename': os.path.join(
                os.environ.get('LOG_DIR', '/logs'),
                os.environ.get('BASE_LOG_FILE', 'app'),
            ),
            'suffix_filename': '.'.join(
                (e for e in (os.environ.get('INSTANCE_NAME'), 'log') if e)
            ),
            'when': 'h',
        },
        'logstash' : {
            'level': 'INFO',
            'class': 'libutil.handlers.UDPLogstashHandler',
            'formatter': 'logstash',
            'host': 'stats-2',
            'port': 3333,
        }
    },
    'loggers': {
        '': {
            # 'handlers': ['logstash', 'rotate_file'],
            'handlers': ['rotate_file'],
            'level': 'DEBUG',
        },
        'pika': {
            'level': 'INFO',
        },
        'iso8601.iso8601': {
            'level': 'INFO',
        },
        'rabbitmq.exchange.monitor.fanout': {
            'level': 'WARNING',
        },
    }
}

TEST_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s,%(msecs)03d %(levelname)-8s %(name)s  %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S',
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(levelname)-8s %(name)s  %(message)s',
            'log_colors' : {
                'DEBUG':    'green',
                #'INFO':     'white',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'purple',
            }
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'colored',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console',],
            'level': 'DEBUG',
        },
        'pika': {
            'level': 'INFO',
        },
        'iso8601.iso8601': {
            'level': 'INFO',
        },
        'rabbitmq.exchange.monitor.fanout': {
            'level': 'WARNING',
        },
    }
}

LOGGING = {
    'dev' : DEV_LOGGING,
    'prod' : PROD_LOGGING,
    'test' : TEST_LOGGING,
}

LOG_CONFIG = os.environ.get('LOG_CONFIG', 'dev')

LOG_CONFIG_DICT = LOGGING[LOG_CONFIG]

ALREADY_WRAPPED = False


def init_logging(handlers=None, loggers=None, log_config=None):
    global ALREADY_WRAPPED

    # update loggers and handlers with passed parameters
    # this allows you to set different log level for different modules
    # for example to set all pika modules to INFO level logging...
    # loggers = {'pika' : {'level' : 'INFO'}}
    if handlers is None:
        handlers = {}
    if loggers is None:
        loggers = {}
    if log_config is None:
        log_config = LOG_CONFIG_DICT

    for dest, source in [('handlers', handlers), ('loggers', loggers)]:
        for entry in source:
            if entry not in log_config[dest]:
                log_config[dest][entry] = source[entry]
            else:
                log_config[dest][entry].update(source[entry])


    # #Override the root logger's makeRecord
    # #For compatability with old style geneity logging which purely uses
    # #the root logger. To let us stick our prefix in the root loggers msg.
    # if not ALREADY_WRAPPED:
    #     ALREADY_WRAPPED = True
    #     logging.root.makeRecord = wrapMakeRecord(logging.root.makeRecord)
    #     logging.root.push_prefix = push_prefix
    #     logging.root.pop_prefix = pop_prefix

    logging.config.dictConfig(log_config)

    logging.captureWarnings(True)


def get_logger(logger_name):
    """
        Provides a logger that supports our prefixing
        code. If your code needs to use [push|pop]_prefix
        or calls out to code that does then you should
        use this to get your logger:

            logger = log_util.get_logger(__name__)

        As opposed to:

            logger = logging.getLogger(__name__)
    """
    init_logging()
    return logging.getLogger(logger_name)
