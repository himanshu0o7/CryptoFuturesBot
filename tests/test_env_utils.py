import importlib
import sys
import pytest


def load_env_utils(monkeypatch, secret_key='1'*64):
    monkeypatch.setenv('COINSWITCH_SECRET_KEY', secret_key)
    if 'env_utils' in sys.modules:
        del sys.modules['env_utils']
    return importlib.import_module('env_utils')


def test_check_required_env_vars_success(monkeypatch):
    utils = load_env_utils(monkeypatch)
    monkeypatch.setenv('TEST_VAR', 'value')
    result = utils.check_required_env_vars(['TEST_VAR'])
    assert result == {'TEST_VAR': 'value'}


def test_check_required_env_vars_missing(monkeypatch):
    utils = load_env_utils(monkeypatch)
    monkeypatch.delenv('MISSING_VAR', raising=False)
    with pytest.raises(ValueError):
        utils.check_required_env_vars(['MISSING_VAR'])
