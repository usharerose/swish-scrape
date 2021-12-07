# Copyright (c) 2021 usharerose. All rights reserved.
import copy
from importlib import import_module
import logging
import os
import types

from swish_task_queue.conf import default_settings


logger = logging.getLogger(__name__)


ENVIRONMENT_VARIABLE = "SWISH_TASK_SETTINGS_MODULE"
DEFAULT_TASK_SETTINGS_MODULE = 'task_queue_config'


_celery_config_vars = ('broker_url',)


def _load_module_to_dict(settings_dict, module, update_dict_value=False):
    for var_key in dir(module):
        if var_key in _celery_config_vars or var_key.isupper():
            var_value = copy.deepcopy(getattr(module, var_key))
            if var_key in settings_dict and (isinstance(var_value, dict) and isinstance(settings_dict[var_key], dict)):
                if update_dict_value:
                    settings_dict[var_key].update(var_value)
            else:
                settings_dict[var_key.lower()] = var_value
    return settings_dict


def _get_settings():
    settings_module_name = os.environ.get(ENVIRONMENT_VARIABLE,
                                          DEFAULT_TASK_SETTINGS_MODULE)
    initial_settings_dict = {}
    settings_dict = _load_module_to_dict(initial_settings_dict, default_settings)

    try:
        customized_settings = import_module(settings_module_name)
        settings_dict = _load_module_to_dict(settings_dict, customized_settings, update_dict_value=True)
    except Exception:  # NOQA
        logger.exception(f'fail to load Swish task queue settings from \'{settings_module_name}\'')
        raise

    settings_module = types.ModuleType('TaskContext', 'Module created to provide a context for tasks.')
    settings_module.__dict__.update(settings_dict)
    return settings_module


settings = _get_settings()
