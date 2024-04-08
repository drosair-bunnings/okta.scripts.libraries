"""Script to setup logging for the application"""
import logging.config
from logging_config_defaults import DEFAULT_LOG_LEVEL
from logging_config_defaults import REQUESTS_LOG_LEVEL
from logging_config_defaults import DEFAULT_LOG_OUTPUT_FILE

class LevelOnlyFilter:  # pylint: disable=too-few-public-methods
    """Class used to set the log filter levels"""

    def __init__(self, level):
        """Constructor for the LevelOnlyFilter class"""
        self.level = level

    def filter(self, record):
        """Function that checks if the record's filter level
            matches the currently set filter level"""
        return record.levelno == self.level


# Define the TRACE log level
TRACE = 5
logging.addLevelName(5, "TRACE")

# Get the logger for 'requests' module
requests_logger = logging.getLogger("requests")

# Set the logging level to WARNING
requests_logger.setLevel(REQUESTS_LOG_LEVEL)

LOGGING_CONFIG = {
    "version": 1,
    "loggers": {
        "": {  # root logger
            "level": DEFAULT_LOG_LEVEL,
            "propagate": False,
            "handlers": ["stream_handler"],
        },
        "custom_logger": {
            "level": DEFAULT_LOG_LEVEL,
            "propagate": False,
            "handlers": ["stream_handler", "file_handler"],
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": DEFAULT_LOG_LEVEL,
            # "filters": ["only_warning"],
            "formatter": "default_formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": DEFAULT_LOG_OUTPUT_FILE,
            "mode": "a",
            "level": DEFAULT_LOG_LEVEL,
            "formatter": "default_formatter",
        },
        'rotating_to_file': {
            'level': DEFAULT_LOG_LEVEL,
            'class': "logging.handlers.RotatingFileHandler",
            'formatter': 'default_formatter',
            "filename": "output.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": True
        },
    },
    "filters": {
        "only_warning": {
            "()": LevelOnlyFilter,
            "level": logging.WARN,
        },
        "only_trace": {
            "()": LevelOnlyFilter,
            "level": TRACE,
        },
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s-%(levelname)s::%(module)s|%(lineno)s:: %(message)s",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("custom_logger")
