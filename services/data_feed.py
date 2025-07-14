"""
Live data feed service for CryptoFuturesBot
Handles real-time market data and WebSocket connections
"""

import asyncio
import json
import logging
import time
import websocket
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from threading import Thread, Event
import requests

from utils.logging_setup import LoggerMixin
from utils.error_handler import retry, handle_exceptions

logger = logging.getLogger(__name__)


@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    price: float
    volume: float
    timestamp: int
    bid: Optional[float] = None
    ask: Optional[float] = None
    change_24h: Optional[float] = None
    change_pct_24h: Optional[float] = None


@dataclass
class OrderBookData:
    """Order book data structure"""
    symbol: str
    bids: List[List[float]]  # [price, quantity]
    asks: List[List[float]]  # [price, quantity]
    timestamp: int


@dataclass
class TradeData:
    """Trade data structure"""
    symbol: str
    price: float
    quantity: float
    side: str  # BUY or SELL
    timestamp: int
    trade_id: Optional[str] = None


class LiveDataFeed(LoggerMixin):
    """Live data feed manager"""
    
    def __init__(self, api_base_url: str = "https://api.coinswitch.co"):
        """
        Initialize data feed
        
        Args:
            api_base_url: Base URL for REST API
        """
        self.api_base_url = api_base_url
        self.ws_url = "wss://api.coinswitch.co/ws"
        self.ws_connection = None
        self.is_connected = False
        self.subscriptions = set()
        self.callbacks = {}
        self.stop_event = Event()
        self.ws_thread = None
        
        # Data storage
        self.latest_prices = {}
        self.order_books = {}
        self.recent_trades = {}
    
    @handle_exceptions()
    def get_live_price(self, symbol: str = "BTCUSDT") -> Optional[float]:
        """
        Get current live price for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Current price or None if error
        """
        try:
            # Try to get from local cache first
            if symbol in self.latest_prices:
                data = self.latest_prices[symbol]
                # Check if data is recent (within 10 seconds)
                if time.time() - data.timestamp < 10:
                    return data.price
            
            # Fetch from REST API
            return self._fetch_price_rest(symbol)
            
        except Exception as e:
            self.logger.error(f"Failed to get live price for {symbol}: {e}")
            return None
    
    def _fetch_price_rest(self, symbol: str) -> Optional[float]:
        """Fetch price via REST API"""
        try:
            url = f"{self.api_base_url}/v2/price"
            params = {"symbol": symbol}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = float(data.get('price', 0))
            
            # Update local cache
            self.latest_prices[symbol] = MarketData(
                symbol=symbol,
                price=price,
                volume=0,
                timestamp=int(time.time())
            )
            
            return price
            
        except Exception as e:
            self.logger.error(f"REST API price fetch failed for {symbol}: {e}")
            return None
    
    @handle_exceptions()
    def get_market_data(self, symbol: str) -> Optional[MarketData]:
        """
        Get comprehensive market data for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            MarketData object or None
        """
        try:
            url = f"{self.api_base_url}/v2/ticker"
            params = {"symbol": symbol}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            market_data = MarketData(
                symbol=symbol,
                price=float(data.get('price', 0)),
                volume=float(data.get('volume', 0)),
                timestamp=int(time.time()),
                bid=float(data.get('bid', 0)) if data.get('bid') else None,
                ask=float(data.get('ask', 0)) if data.get('ask') else None,
                change_24h=float(data.get('change', 0)) if data.get('change') else None,
                change_pct_24h=float(data.get('changePercent', 0)) if data.get('changePercent') else None
            )
            
            # Update local cache
            self.latest_prices[symbol] = market_data
            
            return market_data
            
        except Exception as e:
            self.logger.error(f"Failed to get market data for {symbol}: {e}")
            return None
    
    @handle_exceptions()
    def get_order_book(self, symbol: str, depth: int = 20) -> Optional[OrderBookData]:
        """
        Get order book data for a symbol
        
        Args:
            symbol: Trading symbol
            depth: Order book depth
            
        Returns:
            OrderBookData object or None
        """
        try:
            url = f"{self.api_base_url}/v2/orderbook"
            params = {"symbol": symbol, "depth": depth}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            order_book = OrderBookData(
                symbol=symbol,
                bids=data.get('bids', []),
                asks=data.get('asks', []),
                timestamp=int(time.time())
            )
            
            # Update local cache
            self.order_books[symbol] = order_book
            
            return order_book
            
        except Exception as e:
            self.logger.error(f"Failed to get order book for {symbol}: {e}")
            return None
    
    def start_websocket(self) -> bool:
        """
        Start WebSocket connection for real-time data
        
        Returns:
            True if started successfully
        """
        try:
            if self.is_connected:
                self.logger.warning("WebSocket already connected")
                return True
            
            self.stop_event.clear()
            self.ws_thread = Thread(target=self._websocket_worker, daemon=True)
            self.ws_thread.start()
            
            # Wait for connection
            for _ in range(50):  # Wait up to 5 seconds
                if self.is_connected:
                    self.logger.info("WebSocket connected successfully")
                    return True
                time.sleep(0.1)
            
            self.logger.error("WebSocket connection timeout")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to start WebSocket: {e}")
            return False
    
    def stop_websocket(self):
        """Stop WebSocket connection"""
        try:
            self.stop_event.set()
            self.is_connected = False
            
            if self.ws_connection:
                self.ws_connection.close()
            
            if self.ws_thread and self.ws_thread.is_alive():
                self.ws_thread.join(timeout=5)
            
            self.logger.info("WebSocket disconnected")
            
        except Exception as e:
            self.logger.error(f"Error stopping WebSocket: {e}")
    
    def _websocket_worker(self):
        """WebSocket worker thread"""
        try:
            self.ws_connection = websocket.WebSocketApp(
                self.ws_url,
                on_open=self._on_ws_open,
                on_message=self._on_ws_message,
                on_error=self._on_ws_error,
                on_close=self._on_ws_close
            )
            
            self.ws_connection.run_forever()
            
        except Exception as e:
            self.logger.error(f"WebSocket worker error: {e}")
            self.is_connected = False
    
    def _on_ws_open(self, ws):
        """WebSocket open handler"""
        self.logger.info("WebSocket connection opened")
        self.is_connected = True
        
        # Re-subscribe to all channels
        for subscription in self.subscriptions:
            self._send_subscription(subscription)
    
    def _on_ws_message(self, ws, message):
        """WebSocket message handler"""
        try:
            data = json.loads(message)
            self._process_ws_message(data)
            
        except Exception as e:
            self.logger.error(f"WebSocket message processing error: {e}")
    
    def _on_ws_error(self, ws, error):
        """WebSocket error handler"""
        self.logger.error(f"WebSocket error: {error}")
        self.is_connected = False
    
    def _on_ws_close(self, ws, close_status_code, close_msg):
        """WebSocket close handler"""
        self.logger.info(f"WebSocket closed: {close_status_code} - {close_msg}")
        self.is_connected = False
        
        # Attempt reconnection if not intentionally stopped
        if not self.stop_event.is_set():
            self.logger.info("Attempting WebSocket reconnection...")
            time.sleep(5)
            self._websocket_worker()
    
    def _process_ws_message(self, data: Dict[str, Any]):
        """Process incoming WebSocket message"""
        try:
            msg_type = data.get('type', '')
            symbol = data.get('symbol', '')
            
            if msg_type == 'ticker':
                # Process ticker data
                market_data = MarketData(
                    symbol=symbol,
                    price=float(data.get('price', 0)),
                    volume=float(data.get('volume', 0)),
                    timestamp=int(time.time()),
                    change_24h=float(data.get('change', 0)) if data.get('change') else None,
                    change_pct_24h=float(data.get('changePercent', 0)) if data.get('changePercent') else None
                )
                
                self.latest_prices[symbol] = market_data
                
                # Call registered callbacks
                self._trigger_callbacks('ticker', symbol, market_data)
                
            elif msg_type == 'orderbook':
                # Process order book data
                order_book = OrderBookData(
                    symbol=symbol,
                    bids=data.get('bids', []),
                    asks=data.get('asks', []),
                    timestamp=int(time.time())
                )
                
                self.order_books[symbol] = order_book
                self._trigger_callbacks('orderbook', symbol, order_book)
                
            elif msg_type == 'trade':
                # Process trade data
                trade_data = TradeData(
                    symbol=symbol,
                    price=float(data.get('price', 0)),
                    quantity=float(data.get('quantity', 0)),
                    side=data.get('side', ''),
                    timestamp=int(time.time()),
                    trade_id=data.get('id')
                )
                
                # Store recent trades
                if symbol not in self.recent_trades:
                    self.recent_trades[symbol] = []
                
                self.recent_trades[symbol].append(trade_data)
                
                # Keep only last 100 trades
                if len(self.recent_trades[symbol]) > 100:
                    self.recent_trades[symbol] = self.recent_trades[symbol][-100:]
                
                self._trigger_callbacks('trade', symbol, trade_data)
                
        except Exception as e:
            self.logger.error(f"WebSocket message processing error: {e}")
    
    def subscribe_ticker(self, symbol: str, callback: Optional[Callable] = None):
        """Subscribe to ticker updates for a symbol"""
        subscription = f"ticker:{symbol}"
        self.subscriptions.add(subscription)
        
        if callback:
            self.callbacks[f"ticker_{symbol}"] = callback
        
        if self.is_connected:
            self._send_subscription(subscription)
    
    def subscribe_orderbook(self, symbol: str, callback: Optional[Callable] = None):
        """Subscribe to order book updates for a symbol"""
        subscription = f"orderbook:{symbol}"
        self.subscriptions.add(subscription)
        
        if callback:
            self.callbacks[f"orderbook_{symbol}"] = callback
        
        if self.is_connected:
            self._send_subscription(subscription)
    
    def subscribe_trades(self, symbol: str, callback: Optional[Callable] = None):
        """Subscribe to trade updates for a symbol"""
        subscription = f"trades:{symbol}"
        self.subscriptions.add(subscription)
        
        if callback:
            self.callbacks[f"trade_{symbol}"] = callback
        
        if self.is_connected:
            self._send_subscription(subscription)
    
    def _send_subscription(self, subscription: str):
        """Send subscription message to WebSocket"""
        try:
            if self.ws_connection and self.is_connected:
                message = {
                    "method": "SUBSCRIBE",
                    "params": [subscription]
                }
                self.ws_connection.send(json.dumps(message))
                self.logger.debug(f"Sent subscription: {subscription}")
                
        except Exception as e:
            self.logger.error(f"Failed to send subscription {subscription}: {e}")
    
    def _trigger_callbacks(self, data_type: str, symbol: str, data: Any):
        """Trigger registered callbacks for data updates"""
        try:
            callback_key = f"{data_type}_{symbol}"
            if callback_key in self.callbacks:
                callback = self.callbacks[callback_key]
                callback(data)
                
        except Exception as e:
            self.logger.error(f"Callback error for {data_type}_{symbol}: {e}")
    
    def get_cached_price(self, symbol: str) -> Optional[float]:
        """Get cached price for a symbol"""
        if symbol in self.latest_prices:
            return self.latest_prices[symbol].price
        return None
    
    def get_cached_order_book(self, symbol: str) -> Optional[OrderBookData]:
        """Get cached order book for a symbol"""
        return self.order_books.get(symbol)
    
    def get_recent_trades(self, symbol: str, limit: int = 50) -> List[TradeData]:
        """Get recent trades for a symbol"""
        if symbol in self.recent_trades:
            return self.recent_trades[symbol][-limit:]
        return []


class MockDataFeed(LiveDataFeed):
    """Mock data feed for testing"""
    
    def __init__(self):
        super().__init__()
        self.mock_prices = {
            "BTCUSDT": 45000.0,
            "ETHUSDT": 2800.0,
            "ADAUSDT": 0.5
        }
    
    def get_live_price(self, symbol: str = "BTCUSDT") -> Optional[float]:
        """Mock implementation that returns fake prices"""
        base_price = self.mock_prices.get(symbol, 50000.0)
        # Add some random variation
        import random
        variation = random.uniform(-0.01, 0.01)  # ±1% variation
        return base_price * (1 + variation)
    
    def get_market_data(self, symbol: str) -> Optional[MarketData]:
        """Mock market data"""
        price = self.get_live_price(symbol)
        if price:
            return MarketData(
                symbol=symbol,
                price=price,
                volume=1000000.0,
                timestamp=int(time.time()),
                bid=price * 0.999,
                ask=price * 1.001,
                change_24h=price * 0.02,
                change_pct_24h=2.0
            )
        return None