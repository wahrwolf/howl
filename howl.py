#!/bin/env python3
"""Multi protocol cli messenger powered by toml and fire
"""
from logging import warning, info, debug
from logging.config import dictConfig
from importlib import import_module
from toml import load
from fire import Fire

from howl.defaults import merge_dicts, LOGGER_CONFIG as DEFAULT_LOGGER_CONFIG, RUNTIME_OPTIONS as DEFAULT_OPTIONS
from howl.Messenger import Messenger

def load_plugins(modules_config):
    info("Loading up plugins:")
    modules = {}
    # Load up modules
    for plugin in modules_config:
        name = plugin['name']
        class_name = plugin['class']
        debug(f"  -Installing: [{name}]")
        try:
            module = import_module(name)
            debug("  -Loaded module")
            class_object = getattr(module, class_name)
            debug("  -Loaded class")

            if not Messenger in class_object.__bases__:
                raise NotImplementedError
            else:
                debug("  -Plugin-Class is valid!")

        except Exception as err:
            warning(err)
            warning(f"  -Failed to load {name}... Skiping it!")
        else:
            modules[name] = class_object
            info(f"  -Installed {name}")
    return modules

def load_accounts(account_config, modules, options):
    # Load all accounts
    accounts = {}
    info("Loading up accounts:")
    for account in account_config:
        name = account["name"]
        module = account["module"]

        params = options
        params.update(account['params'])
        debug(f"  -Activating {name}")

        try:
            debug(f"  Connecting to {module}")
            debug(f"  Using: {params}")
            account_object = modules[module](**params)
            debug(f"  -Init succesfull!")
        except Exception as err:
            warning(err)
            warning(f"  -Failed to load {name}... Skiping it!")
        else:
            accounts[name] = account_object
            info(f"  -Activated {name}")
        finally:
            return accounts

def main(config_path=None):
    # Parse config file
    user_config = load(DEFAULT_OPTIONS["options"]["config"]["path"]
                       if config_path is None else config_path)

    runtime_config = merge_dicts(DEFAULT_OPTIONS, user_config.get("options", {}))

    logger_config = merge_dicts(DEFAULT_LOGGER_CONFIG, user_config.get("logger", {}))
    dictConfig(logger_config)

    debug("Loaded the following user config:")
    debug(user_config)

    debug("Expanded the default runtime option")
    debug(DEFAULT_OPTIONS)
    debug(runtime_config)

    debug("Expanded the default logger options")
    debug(DEFAULT_LOGGER_CONFIG)
    debug(logger_config)

    modules = load_plugins(user_config.get("modules"))
    accounts = load_accounts(user_config.get("accounts"), modules, runtime_config)

    Fire(accounts)

if __name__ == '__main__':
    main()
