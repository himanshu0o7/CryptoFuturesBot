import importlib
import os
import sys

from part1_core import signal_generator as sg
sg = importlib.import_module('signal_generator')


def test_generate_signals_basic():
    data = [
        {'symbol': 'BTCUSDT', 'priceChangePercent': '4', 'quoteVolume': '20000000', 'lastPrice': '50000'},
        {'symbol': 'ETHUSDT', 'priceChangePercent': '-5', 'quoteVolume': '15000000', 'lastPrice': '3000'},
        {'symbol': 'XRPUSDT', 'priceChangePercent': '1', 'quoteVolume': '5000000', 'lastPrice': '0.5'},
    ]
    buys, sells = sg.generate_signals(data)
    assert buys == [{
        'symbol': 'BTCUSDT',
        'change_percent': 4.0,
        'quote_volume': 20000000.0,
        'last_price': 50000.0,
    }]
    assert sells == [{
        'symbol': 'ETHUSDT',
        'change_percent': -5.0,
        'quote_volume': 15000000.0,
        'last_price': 3000.0,
    }]


def test_generate_signals_no_signals():
    data = [
        {'symbol': 'ADAUSDT', 'priceChangePercent': '2', 'quoteVolume': '8000000', 'lastPrice': '1'},
    ]
    buys, sells = sg.generate_signals(data)
    assert buys == []
    assert sells == []

