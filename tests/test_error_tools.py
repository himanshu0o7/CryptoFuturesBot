import os
from unittest.mock import MagicMock

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "x")
os.environ.setdefault("TELEGRAM_CHAT_ID", "1")

import pytest

from infra import error_autofix as autofix
from infra import error_detector as detector


def test_ensure_env(tmp_path, monkeypatch):
    sample = tmp_path / ".env.sample"
    sample.write_text("A=1")
    monkeypatch.chdir(tmp_path)
    autofix.ensure_env()
    assert (tmp_path / ".env").read_text() == "A=1"


def test_safe_import_fallback(monkeypatch):
    module_name = "nonexistent_module_xyz"
    result = autofix.safe_import(module_name, fallback="math", retries=1)
    assert result.__name__ == "math"


def test_retry_network_success(monkeypatch):
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ConnectionError("fail")
        return 42

    result = autofix.retry_network(flaky, retries=3, delay=0)
    assert result == 42
    assert calls["n"] == 2


def test_safe_json_loads_error(tmp_path, monkeypatch):
    messages = []
    log_file = tmp_path / "err.log"
    monkeypatch.setattr(detector, "LOG_FILE", str(log_file))
    monkeypatch.setattr(detector, "notify", lambda msg: messages.append(msg))
    result = detector.safe_json_loads("{bad}")
    assert result is None
    assert messages
    assert "JSON decode error" in log_file.read_text()


def test_check_balance(monkeypatch, tmp_path):
    messages = []
    log_file = tmp_path / "err.log"
    monkeypatch.setattr(detector, "LOG_FILE", str(log_file))
    monkeypatch.setattr(detector, "notify", lambda msg: messages.append(msg))
    assert not detector.check_balance(1, 5)
    assert messages
    assert "Insufficient balance" in log_file.read_text()
