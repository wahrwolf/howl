#!/bin/env python3
from logging import getLogger
from logging.config import dictConfig
from importlib import import_module
from toml import load

from howl.defaults import logger_config as DEFAULT_LOGGER_CONFIG
from howl.Messenger import Messenger

# Parse commandline args
config_path = "./howl.toml"

# Parse config file
CONFIG = load(config_path)

try:
    LOGGER_CONFIG = CONFIG["options"]["logger"]
except KeyError:
    LOGGER_CONFIG = DEFAULT_LOGGER_CONFIG
    # default fallback logging config
finally:
    dictConfig(LOGGER_CONFIG)

# Init logger
logger = getLogger()

logger.debug("Loading up modules...")
modules = {}

# Load up modules
for plugin in CONFIG["modules"]:
    name = plugin['name']
    class_name = plugin['class']
    logger.debug(f"Installing plugin: [{name}]")
    try:
        module = import_module(name)
        logger.debug("  -Loaded module")
        class_object = getattr(module, class_name)
        logger.debug("  -Loaded class")

        if not Messenger in class_object.__bases__:
            raise NotImplementedError
        else:
            logger.debug("  -Plugin-Class is valid!")

    except Exception as err:
        logger.debug(err)
        logger.debug(f"  -Failed to load {name}... Skiping it!")
    else:
        modules[name] = None
        logger.debug(f"  -Installed {name}")

# Load all accounts
logger.debug("Loading up accounts...")
for account in CONFIG["accounts"]:
    logger.debug(f"  {account['name']}: Loading up module {account['module']}")
