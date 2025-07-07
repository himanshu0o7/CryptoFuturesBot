import pytest

# Import test modules so their tests are registered
from tests import test_indicator_api, test_env_utils, test_telegram_bot

if __name__ == "__main__":
    modules = [test_indicator_api, test_env_utils, test_telegram_bot]
    paths = [m.__file__ for m in modules]
    raise SystemExit(pytest.main(paths))
