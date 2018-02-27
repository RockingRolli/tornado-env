import os
import pytest

from tornado_env.config import get_from_env, parse_config, env, NoValue, parse_env_file
from tornado_env.exceptions import ConfigError


str_name = 'test_string'
str_key = 'TEST_STRING'
str_value = 'muaythai'

bool_name = 'test_bool'
bool_key = 'TEST_BOOL'
bool_value = True


def test_read_env_file(pathlib_tmpdir):
    env_file = pathlib_tmpdir / '.env'

    with open(env_file, 'w') as f:
        f.write('{}={}'.format(str_key, str_value))

    parse_env_file(env_file)

    assert os.environ[str_key] == str_value


def test_raise_error_on_missing_config_file(pathlib_tmpdir):
    env_file = pathlib_tmpdir / '.env'
    with pytest.raises(ConfigError):
        parse_env_file(env_file)


def test_get_str():
    os.environ.setdefault(str_key, str_value)
    assert get_from_env(**env(str_key)) == str_value


def test_get_bool():
    os.environ.setdefault(bool_key, str(bool_value))
    assert get_from_env(**env(bool_key, cast=bool)) is True


def test_get_default():
    assert get_from_env(**env(str_key, default=str_value)) == str_value


def test_raise_error_when_no_default_set():
    with pytest.raises(ConfigError):
        get_from_env(**env(str_key))


def test_no_value():
    no_value = NoValue()
    assert str(no_value) == '<NoValue>'


def test_parse_config_with_env_file(app):
    config = {
        str_name: env(str_key)
    }

    os.environ.setdefault(str_key, str_value)

    parse_config(app, config)

    assert app.settings[str_name] == str_value


def test_parse_config(app, pathlib_tmpdir):
    env_file = pathlib_tmpdir / '.env'

    config = {
        str_name: env(str_key)
    }

    with open(env_file, 'w') as f:
        f.write('{}={}'.format(str_key, str_value))

    parse_config(app, config, env_file)

    assert app.settings[str_name] == str_value

