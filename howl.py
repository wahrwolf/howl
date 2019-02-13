#!/bin/env python3
from os import system
from logging import getLogger
from logging.config import dictConfig
from importlib import import_module
from toml import load
from fire import Fire

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

logger.debug("Loading up modules:")
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
        modules[name] = class_object
        logger.debug(f"  -Installed {name}")

# Load all accounts
accounts = {}
logger.debug("Loading up accounts:")
for account in CONFIG["accounts"]:
    name = account["name"]
    module = account["module"]
    params = account['params']

    try:
        logger.debug(f"  Connecting to {module}")
        logger.debug(f"  Using: {params}")
        account_object = modules[module](**params)
        logger.debug(f"  -Init succesfull!")
    except Exception as err:
        logger.debug(err)
        logger.debug(f"  -Failed to load {name}... Skiping it!")
    else:
        accounts[name] = account_object
        logger.debug(f"  -Activated {name}")


if __name__ == '__main__':
    Fire(accounts)
