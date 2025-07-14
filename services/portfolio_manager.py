"""
Portfolio management service for CryptoFuturesBot
Handles position tracking, PnL calculation, and portfolio analytics
"""

import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json

from utils.logging_setup import LoggerMixin
from utils.error_handler import handle_exceptions
from utils.telegram_alert import send_pnl_update

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """Position data structure"""
    symbol: str
    side: str  # LONG or SHORT
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    entry_time: str = field(default_factory=lambda: datetime.now().isoformat())
    last_update: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Trade:
    """Trade record structure"""
    symbol: str
    side: str
    quantity: float
    price: float
    fee: float
    timestamp: str
    order_id: str
    pnl: float = 0.0


@dataclass
class PortfolioStats:
    """Portfolio statistics structure"""
    total_value: float
    available_balance: float
    unrealized_pnl: float
    realized_pnl: float
    total_pnl: float
    positions_count: int
    daily_pnl: float
    weekly_pnl: float
    monthly_pnl: float
    max_drawdown: float
    win_rate: float
    total_trades: int


class PortfolioManager(LoggerMixin):
    """Portfolio management system"""
    
    def __init__(self, initial_balance: float = 10000.0, 
                 data_file: str = "portfolio_data.json"):
        """
        Initialize portfolio manager
        
        Args:
            initial_balance: Starting portfolio balance
            data_file: File to persist portfolio data
        """
        self.initial_balance = initial_balance
        self.data_file = data_file
        
        # Portfolio state
        self.positions: Dict[str, Position] = {}
        self.trade_history: List[Trade] = []
        self.balance = initial_balance
        self.equity = initial_balance
        
        # Performance tracking
        self.daily_pnl_history = []
        self.peak_equity = initial_balance
        self.max_drawdown = 0.0
        
        # Load existing data
        self._load_portfolio_data()
    
    @handle_exceptions()
    def update_position(self, symbol: str, current_price: float) -> Optional[Position]:
        """
        Update position with current market price
        
        Args:
            symbol: Trading symbol
            current_price: Current market price
            
        Returns:
            Updated position or None
        """
        if symbol not in self.positions:
            self.logger.warning(f"No position found for {symbol}")
            return None
        
        position = self.positions[symbol]
        position.current_price = current_price
        position.last_update = datetime.now().isoformat()
        
        # Calculate unrealized PnL
        if position.side == "LONG":
            position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
        else:  # SHORT
            position.unrealized_pnl = (position.entry_price - current_price) * position.quantity
        
        self.logger.debug(f"Updated position {symbol}: PnL = {position.unrealized_pnl:.2f}")
        
        # Save data
        self._save_portfolio_data()
        
        return position
    
    @handle_exceptions()
    def add_trade(self, symbol: str, side: str, quantity: float, price: float,
                  fee: float = 0.0, order_id: str = "") -> bool:
        """
        Add a new trade to the portfolio
        
        Args:
            symbol: Trading symbol
            side: Trade side (BUY/SELL)
            quantity: Trade quantity
            price: Trade price
            fee: Trading fee
            order_id: Order ID
            
        Returns:
            True if successful
        """
        try:
            # Create trade record
            trade = Trade(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                fee=fee,
                timestamp=datetime.now().isoformat(),
                order_id=order_id
            )
            
            # Update position
            self._update_position_from_trade(trade)
            
            # Add to history
            self.trade_history.append(trade)
            
            # Update balance
            trade_value = quantity * price
            if side == "BUY":
                self.balance -= (trade_value + fee)
            else:
                self.balance += (trade_value - fee)
            
            self.logger.info(f"Trade added: {side} {quantity} {symbol} @ {price}")
            
            # Save data
            self._save_portfolio_data()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add trade: {e}")
            return False
    
    def _update_position_from_trade(self, trade: Trade):
        """Update position based on new trade"""
        symbol = trade.symbol
        
        if symbol not in self.positions:
            # New position
            if trade.side == "BUY":
                self.positions[symbol] = Position(
                    symbol=symbol,
                    side="LONG",
                    quantity=trade.quantity,
                    entry_price=trade.price,
                    current_price=trade.price
                )
            # Note: SHORT positions would be handled differently
        else:
            # Existing position
            position = self.positions[symbol]
            
            if trade.side == "BUY" and position.side == "LONG":
                # Adding to long position
                total_value = (position.quantity * position.entry_price) + (trade.quantity * trade.price)
                total_quantity = position.quantity + trade.quantity
                position.entry_price = total_value / total_quantity
                position.quantity = total_quantity
                
            elif trade.side == "SELL" and position.side == "LONG":
                # Reducing/closing long position
                if trade.quantity >= position.quantity:
                    # Position closed
                    realized_pnl = (trade.price - position.entry_price) * position.quantity
                    position.realized_pnl += realized_pnl
                    trade.pnl = realized_pnl
                    
                    if trade.quantity > position.quantity:
                        # Excess becomes short position
                        excess_quantity = trade.quantity - position.quantity
                        position.side = "SHORT"
                        position.quantity = excess_quantity
                        position.entry_price = trade.price
                    else:
                        # Position completely closed
                        del self.positions[symbol]
                else:
                    # Partial close
                    realized_pnl = (trade.price - position.entry_price) * trade.quantity
                    position.realized_pnl += realized_pnl
                    position.quantity -= trade.quantity
                    trade.pnl = realized_pnl
    
    @handle_exceptions()
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol"""
        return self.positions.get(symbol)
    
    def get_all_positions(self) -> List[Position]:
        """Get all current positions"""
        return list(self.positions.values())
    
    @handle_exceptions()
    def calculate_portfolio_stats(self) -> PortfolioStats:
        """Calculate comprehensive portfolio statistics"""
        try:
            # Calculate unrealized PnL
            total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
            
            # Calculate realized PnL
            total_realized_pnl = sum(trade.pnl for trade in self.trade_history)
            
            # Calculate total portfolio value
            position_value = sum(pos.quantity * pos.current_price for pos in self.positions.values())
            total_value = self.balance + position_value
            
            # Update equity
            self.equity = total_value
            
            # Update peak equity and max drawdown
            if self.equity > self.peak_equity:
                self.peak_equity = self.equity
            
            current_drawdown = (self.peak_equity - self.equity) / self.peak_equity
            if current_drawdown > self.max_drawdown:
                self.max_drawdown = current_drawdown
            
            # Calculate time-based PnL
            daily_pnl = self._calculate_period_pnl(days=1)
            weekly_pnl = self._calculate_period_pnl(days=7)
            monthly_pnl = self._calculate_period_pnl(days=30)
            
            # Calculate win rate
            profitable_trades = len([t for t in self.trade_history if t.pnl > 0])
            total_trades = len(self.trade_history)
            win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
            
            stats = PortfolioStats(
                total_value=total_value,
                available_balance=self.balance,
                unrealized_pnl=total_unrealized_pnl,
                realized_pnl=total_realized_pnl,
                total_pnl=total_unrealized_pnl + total_realized_pnl,
                positions_count=len(self.positions),
                daily_pnl=daily_pnl,
                weekly_pnl=weekly_pnl,
                monthly_pnl=monthly_pnl,
                max_drawdown=self.max_drawdown * 100,
                win_rate=win_rate,
                total_trades=total_trades
            )
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to calculate portfolio stats: {e}")
            return PortfolioStats(
                total_value=0, available_balance=0, unrealized_pnl=0,
                realized_pnl=0, total_pnl=0, positions_count=0,
                daily_pnl=0, weekly_pnl=0, monthly_pnl=0,
                max_drawdown=0, win_rate=0, total_trades=0
            )
    
    def _calculate_period_pnl(self, days: int) -> float:
        """Calculate PnL for a specific period"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_time.isoformat()
            
            period_trades = [
                trade for trade in self.trade_history 
                if trade.timestamp >= cutoff_str
            ]
            
            return sum(trade.pnl for trade in period_trades)
            
        except Exception:
            return 0.0
    
    @handle_exceptions()
    def send_portfolio_update(self):
        """Send portfolio update via Telegram"""
        try:
            stats = self.calculate_portfolio_stats()
            
            # Find the position with highest PnL for the alert
            if self.positions:
                best_position = max(self.positions.values(), key=lambda p: p.unrealized_pnl)
                
                send_pnl_update(
                    symbol=best_position.symbol,
                    pnl=best_position.unrealized_pnl,
                    percentage=(best_position.unrealized_pnl / (best_position.quantity * best_position.entry_price)) * 100,
                    entry_price=best_position.entry_price,
                    current_price=best_position.current_price
                )
            
        except Exception as e:
            self.logger.error(f"Failed to send portfolio update: {e}")
    
    def _save_portfolio_data(self):
        """Save portfolio data to file"""
        try:
            data = {
                'balance': self.balance,
                'equity': self.equity,
                'peak_equity': self.peak_equity,
                'max_drawdown': self.max_drawdown,
                'positions': {
                    symbol: {
                        'symbol': pos.symbol,
                        'side': pos.side,
                        'quantity': pos.quantity,
                        'entry_price': pos.entry_price,
                        'current_price': pos.current_price,
                        'unrealized_pnl': pos.unrealized_pnl,
                        'realized_pnl': pos.realized_pnl,
                        'entry_time': pos.entry_time,
                        'last_update': pos.last_update
                    }
                    for symbol, pos in self.positions.items()
                },
                'trade_history': [
                    {
                        'symbol': trade.symbol,
                        'side': trade.side,
                        'quantity': trade.quantity,
                        'price': trade.price,
                        'fee': trade.fee,
                        'timestamp': trade.timestamp,
                        'order_id': trade.order_id,
                        'pnl': trade.pnl
                    }
                    for trade in self.trade_history
                ]
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save portfolio data: {e}")
    
    def _load_portfolio_data(self):
        """Load portfolio data from file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.balance = data.get('balance', self.initial_balance)
            self.equity = data.get('equity', self.initial_balance)
            self.peak_equity = data.get('peak_equity', self.initial_balance)
            self.max_drawdown = data.get('max_drawdown', 0.0)
            
            # Load positions
            for symbol, pos_data in data.get('positions', {}).items():
                self.positions[symbol] = Position(**pos_data)
            
            # Load trade history
            for trade_data in data.get('trade_history', []):
                self.trade_history.append(Trade(**trade_data))
            
            self.logger.info(f"Loaded portfolio data: {len(self.positions)} positions, {len(self.trade_history)} trades")
            
        except FileNotFoundError:
            self.logger.info("No existing portfolio data found, starting fresh")
        except Exception as e:
            self.logger.error(f"Failed to load portfolio data: {e}")
    
    def get_position_summary(self) -> Dict[str, Any]:
        """Get summary of all positions"""
        try:
            positions_data = []
            for position in self.positions.values():
                pnl_pct = (position.unrealized_pnl / (position.quantity * position.entry_price)) * 100
                positions_data.append({
                    'symbol': position.symbol,
                    'side': position.side,
                    'quantity': position.quantity,
                    'entry_price': position.entry_price,
                    'current_price': position.current_price,
                    'unrealized_pnl': position.unrealized_pnl,
                    'pnl_percentage': pnl_pct
                })
            
            return {
                'positions': positions_data,
                'total_positions': len(positions_data),
                'total_unrealized_pnl': sum(pos.unrealized_pnl for pos in self.positions.values())
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get position summary: {e}")
            return {'positions': [], 'total_positions': 0, 'total_unrealized_pnl': 0}
    
    def close_position(self, symbol: str, price: float) -> bool:
        """
        Close a position at given price
        
        Args:
            symbol: Symbol to close
            price: Closing price
            
        Returns:
            True if successful
        """
        if symbol not in self.positions:
            self.logger.warning(f"No position to close for {symbol}")
            return False
        
        position = self.positions[symbol]
        
        # Add closing trade
        side = "SELL" if position.side == "LONG" else "BUY"
        return self.add_trade(
            symbol=symbol,
            side=side,
            quantity=position.quantity,
            price=price,
            order_id=f"CLOSE_{symbol}_{int(time.time())}"
        )