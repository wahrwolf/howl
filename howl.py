#!/bin/env python3
from os import system
from logging import getLogger
from logging.config import dictConfig
from importlib import import_module
from toml import load
from fire import Fire

from howl.defaults import logger_config as DEFAULT_LOGGER_CONFIG
from howl.Messenger import Messenger

def load_plugins(modules_config, logger):
    logger.debug("Loading up modules:")
    modules = {}
    # Load up modules
    for plugin in modules_config:
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
    return modules

def load_accounts(account_config, modules, logger):
    # Load all accounts
    accounts = {}
    logger.debug("Loading up accounts:")
    for account in account_config:
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
        finally:
            return accounts

def main( config_path = "./howl.toml"):
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

    modules = load_plugins(CONFIG["modules"], logger)
    accounts = load_accounts(CONFIG["accounts"], modules, logger)

    Fire(accounts)

if __name__ == '__main__':
    main()
