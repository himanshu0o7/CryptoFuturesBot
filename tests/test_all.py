import pytest

 codex/add-tests-for-telegram-and-env_utils
# Import test modules so their tests are registered
from tests import test_indicator_api, test_env_utils, test_telegram_bot

if __name__ == "__main__":
    modules = [test_indicator_api, test_env_utils, test_telegram_bot]
    paths = [m.__file__ for m in modules]
    raise SystemExit(pytest.main(paths))

# Import individual test modules so they can be run together
import tests.test_signal_generation
import tests.test_telegram_formatting
import tests.test_env_validation
import tests.test_indicator_api


if __name__ == "__main__":
    pytest.main([
        tests.test_signal_generation.__file__,
        tests.test_telegram_formatting.__file__,
        tests.test_env_validation.__file__,
        tests.test_indicator_api.__file__,
    ])

master
