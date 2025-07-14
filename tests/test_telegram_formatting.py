import os


def test_alert_new_signals_format(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "chat")
    import telegram_bot


def test_alert_new_signals_format(monkeypatch):
    messages = {}

    def fake_send_message(text):
        messages["text"] = text

    monkeypatch.setattr(telegram_bot, "send_message", fake_send_message)

    buy = [
        {
            "symbol": "BTCUSDT",
            "change_percent": 5,
            "quote_volume": 20000000,
            "last_price": 50000,
        }
    ]
    sell = [
        {
            "symbol": "ETHUSDT",
            "change_percent": -4,
            "quote_volume": 15000000,
            "last_price": 3000,
        }
    ]

    telegram_bot.alert_new_signals(buy, sell)

    expected_lines = [
        "<b>🚀 New Trading Signals</b>",
        "\n<b>Buy Signals</b>",
        "✅ BTCUSDT | 5% | Vol $20,000,000 | Price 50000",
        "\n<b>Sell Signals</b>",
        "🔻 ETHUSDT | -4% | Vol $15,000,000 | Price 3000",
    ]
    expected = "\n".join(expected_lines)
    assert messages["text"] == expected
