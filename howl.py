#!/bin/env python3
"""Multi protocol cli messenger powered by toml and fire
"""
from logging import getLogger
from logging.config import dictConfig
from importlib import import_module
from toml import load
from fire import Fire

from howl.defaults import LOGGER_CONFIG as DEFAULT_LOGGER_CONFIG, RUNTIME_OPTIONS as DEFAULT_OPTIONS
from howl.Messenger import Messenger

def load_plugins(modules_config):
    logger = getLogger()
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

def load_accounts(account_config, modules, options):
    logger = getLogger()
    # Load all accounts
    accounts = {}
    logger.debug("Loading up accounts:")
    for account in account_config:
        name = account["name"]
        module = account["module"]

        params = {"options":options}
        params.update(account['params'])

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

    runtime_config = DEFAULT_OPTIONS
    runtime_config.update(CONFIG.get("options"))

    logger_config = DEFAULT_LOGGER_CONFIG
    logger_config.update(runtime_config.get("logger", {}))
    dictConfig(logger_config)


    # Init logger
    logger = getLogger()

    modules = load_plugins(CONFIG.get("modules"))
    accounts = load_accounts(CONFIG.get("accounts"), modules, runtime_config)

    Fire(accounts)

if __name__ == '__main__':
    main()
