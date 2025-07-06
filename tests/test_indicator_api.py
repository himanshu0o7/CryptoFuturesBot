import importlib
import sys
import os
import json
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import ed25519

# helper to reload module with patched env

def load_api_utils(monkeypatch, secret='1'*64, api_key='key'):
    monkeypatch.setenv('COINSWITCH_SECRET_KEY', secret)
    monkeypatch.setenv('COINSWITCH_API_KEY', api_key)
    if 'coinswitch_api_utils' in sys.modules:
        del sys.modules['coinswitch_api_utils']
    return importlib.import_module('coinswitch_api_utils')


def test_generate_signals():
    sys.path.append(os.path.abspath('part1_core'))
    sg = importlib.import_module('signal_generator')
    data = [
        {'symbol': 'BTCUSDT', 'priceChangePercent': '5', 'quoteVolume': '20000000', 'lastPrice': '50000'},
        {'symbol': 'ETHUSDT', 'priceChangePercent': '-4', 'quoteVolume': '15000000', 'lastPrice': '3000'},
        {'symbol': 'XRPUSDT', 'priceChangePercent': '1', 'quoteVolume': '5000000', 'lastPrice': '0.5'}
    ]
    buys, sells = sg.generate_signals(data)
    assert len(buys) == 1
    assert len(sells) == 1
    assert buys[0]['symbol'] == 'BTCUSDT'
    assert sells[0]['symbol'] == 'ETHUSDT'


def test_get_signature(monkeypatch):
    with patch('time.time', return_value=1700000000.0):
        api = load_api_utils(monkeypatch)
        sig, epoch = api.get_signature('GET', '/test', {'a': '1'}, {})
    msg_endpoint = '/test?a=1'
    payload_str = json.dumps({}, separators=(',', ':'), sort_keys=True)
    msg = 'GET' + msg_endpoint + payload_str
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex('1'*64))
    expected = sk.sign(msg.encode()).hex()
    assert sig == expected
    assert epoch == str(int(1700000000.0 * 1000))


def test_send_request_success(monkeypatch):
    with patch('time.time', return_value=1700000000.0):
        api = load_api_utils(monkeypatch)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'ok': True}
        with patch('coinswitch_api_utils.requests.get', return_value=mock_resp) as m:
            result = api.send_request('GET', '/test', {'a': '1'})
            assert result == {'ok': True}
            m.assert_called_once()


def test_send_request_error(monkeypatch):
    with patch('time.time', return_value=1700000000.0):
        api = load_api_utils(monkeypatch)
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = 'error'
        with patch('coinswitch_api_utils.requests.get', return_value=mock_resp):
            result = api.send_request('GET', '/test', {'a': '1'})
            assert result is None

