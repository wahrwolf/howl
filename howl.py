#!/bin/env python3
from logging import getLogger
from logging.config import dictConfig
from toml import load

from howl.defaults import logger_config as DEFAULT_LOGGER_CONFIG

# Parse commandline args
config_path = "./howl.toml"

# Parse config file
CONFIG = load(config_path)

try:
    LOGGER_CONFIG = CONFIG["options"]["logger"]
except KeyError:
    LOGGER_CONFIG = DEFAULT_LOGGER_CONFIG
    # default fallback logging config
finally :
    dictConfig(LOGGER_CONFIG)

# Init logger
logger = getLogger()

# Load all accounts
logger.debug(CONFIG)

