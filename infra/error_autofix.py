import importlib
import os
import shutil
import time
from typing import Any, Callable

ENV_FILE = ".env"
SAMPLE_FILE = ".env.sample"


def ensure_env() -> None:
    """Create .env from sample if it does not exist."""
    if not os.path.exists(ENV_FILE) and os.path.exists(SAMPLE_FILE):
        shutil.copy(SAMPLE_FILE, ENV_FILE)


def safe_import(name: str, fallback: str | None = None, retries: int = 3, delay: float = 1.0):
    """Import module with retries and optional fallback."""
    for attempt in range(retries):
        try:
            return importlib.import_module(name)
        except Exception:
            if attempt == retries - 1:
                if fallback:
                    return importlib.import_module(fallback)
                raise
            time.sleep(delay)
    raise ImportError(name)


def retry_network(func: Callable[..., Any], *args, retries: int = 3, delay: float = 5.0, **kwargs) -> Any:
    """Retry a network operation if it fails."""
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
