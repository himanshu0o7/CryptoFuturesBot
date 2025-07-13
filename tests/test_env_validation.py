import pytest
from env_utils import check_required_env_vars


def test_check_required_env_vars_success(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "value")
    result = check_required_env_vars(["TEST_VAR"])
    assert result == {"TEST_VAR": "value"}


def test_check_required_env_vars_missing(monkeypatch):
    monkeypatch.delenv("MISSING_VAR", raising=False)
    with pytest.raises(ValueError):
        check_required_env_vars(["MISSING_VAR"])
