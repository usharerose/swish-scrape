# Copyright (c) 2021 usharerose. All rights reserved.
"""
Configuration Object
"""
import importlib
import logging
import os
import re
import traceback


logger = logging.getLogger(__name__)


ENVIRONMENT_VARIABLE = 'SWISH_SETTINGS_MODULE'
KEY_LENGTH_MAXIMUM = 100


def _convert(legacy_value, latest_value):
    """
    convert the data type of latest value according to legacy one
    """
    if isinstance(legacy_value, bool):
        return _str_to_bool(latest_value)
    if isinstance(legacy_value, int):
        return _base_convert(latest_value, int)
    if isinstance(legacy_value, float):
        return _base_convert(latest_value, float)
    return latest_value


def _base_convert(value, func):
    try:
        return func(value)
    except Exception:  # NOQA
        logger.exception('Exception in _convert due to: {}'.format(traceback.format_exc()))
        raise


def _str_to_bool(input_str):
    """
    convert string to bool
    """
    target = input_str.strip().lower()
    mapping = {'true': True, 'false': False}
    converted_value = mapping.get(target, None)
    if converted_value is None:
        raise ValueError('Invalid input {} for converting to bool'.format(input_str))
    return converted_value


def _str_to_array(input_str, delimiter=','):
    """
    convert string to array
    """
    target = input_str.strip()
    if not target:
        return []
    return target.split(delimiter)


def _special_match(input_str, match_pattern=re.compile(r'^[a-zA-Z0-9_-]+$')):
    return re.match(match_pattern, input_str) is not None


class SwishSettings(object):

    def __getattr__(self, key):
        if key not in self.__dict__:
            self._set_up()

        if key not in self.__dict__:
            return super().__getattribute__(key)

        return getattr(self, key)

    def _set_up(self):
        self.__dict__.clear()
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE, 'settings')
        if not settings_module:
            raise Exception(
                f'The settings are not configured, need to define the env var \'{ENVIRONMENT_VARIABLE}\'')

        try:
            imported_module = importlib.import_module(settings_module)
        except Exception:
            logger.exception(f'Settings module is not found in PYTHONPATH: {settings_module}')
            raise

        _pattern = re.compile(r'^[A-Z0-9_-]+$')
        for key in dir(imported_module):
            value = getattr(imported_module, key)
            if key.startswith('__') or not _special_match(key, _pattern):
                pass
            else:
                latest_value = self._get_value_from_env(key, value)
                value = value if latest_value is None else latest_value
            setattr(self, key, value)

    def _get_value_from_env(self, key, value):
        self._validate_key(key)

        if isinstance(value, dict):
            latest_value = self._get_and_update_dict(key, value)
        elif isinstance(value, list):
            latest_value = self._get_list(key, value)
        else:
            latest_value = self._get_ordinary_var(key, value)

        return latest_value

    def _validate_key(self, key):
        if len(key) > KEY_LENGTH_MAXIMUM:
            raise ValueError(
                f'The name\'s length of environment variable \'{key}\' should be less than {KEY_LENGTH_MAXIMUM}')
        if not _special_match(key):
            raise ValueError(
                f'The name of environment variable \'{key}\' contains illegal characters')
        return True

    def _get_and_update_dict(self, parent_key, dict_var):
        if not isinstance(dict_var, dict):
            return {}

        for key in dict_var:
            full_key = f'{parent_key}_{key}'
            dict_var[key] = self._get_value_from_env(full_key, dict_var[key])
        return dict_var

    def _get_list(self, key, value):
        latest_value = os.environ.get(key.upper(), None)
        if latest_value is None:
            return value
        old = value[0] if value else ''
        return [_convert(old, item) for item in _str_to_array(latest_value)]

    def _get_ordinary_var(self, key, value):
        latest_value = os.environ.get(key.upper(), None)
        if latest_value is None:
            return value
        if isinstance(value, (bool, int, float)):
            return _convert(value, latest_value)
        return latest_value


settings = SwishSettings()
