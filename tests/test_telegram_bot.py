import importlib
import sys
from unittest.mock import patch, MagicMock


def load_bot(monkeypatch):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'TOKEN')
    monkeypatch.setenv('TELEGRAM_CHAT_ID', 'CHAT')
    if 'telegram_bot' in sys.modules:
        del sys.modules['telegram_bot']
    return importlib.import_module('telegram_bot')


def test_send_message(monkeypatch):
    bot = load_bot(monkeypatch)
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    with patch('telegram_bot.requests.post', return_value=mock_resp) as mock_post:
        bot.send_message('hi')
        mock_post.assert_called_once_with(
            bot.TELEGRAM_API_URL,
            json={'chat_id': 'CHAT', 'text': 'hi', 'parse_mode': 'HTML'},
            timeout=10
        )


def test_alert_new_signals(monkeypatch):
    bot = load_bot(monkeypatch)
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    with patch('telegram_bot.requests.post', return_value=mock_resp) as mock_post:
        buys = [{'symbol': 'BTC', 'change_percent': '5', 'quote_volume': 1000, 'last_price': '50000'}]
        bot.alert_new_signals(buys, [])
        assert mock_post.called
        sent = mock_post.call_args.kwargs['json']['text']
        assert 'BTC' in sent
