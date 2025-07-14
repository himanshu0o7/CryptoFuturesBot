"""
Base strategy class for CryptoFuturesBot
Provides common interface for all trading strategies
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

from utils.logging_setup import LoggerMixin

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """Trading signal types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE = "CLOSE"


@dataclass
class TradingSignal:
    """Trading signal structure"""
    symbol: str
    signal_type: SignalType
    confidence: float  # 0.0 to 1.0
    price: Optional[float] = None
    quantity: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    reason: str = ""
    timestamp: Optional[str] = None


@dataclass
class MarketContext:
    """Market context for strategy decisions"""
    symbol: str
    current_price: float
    volume: float
    price_history: List[float]
    indicators: Dict[str, Any]
    timestamp: str


class BaseStrategy(ABC, LoggerMixin):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize base strategy
        
        Args:
            name: Strategy name
            parameters: Strategy-specific parameters
        """
        self.name = name
        self.parameters = parameters or {}
        self.active = True
        self.performance_metrics = {
            'total_signals': 0,
            'successful_signals': 0,
            'win_rate': 0.0
        }
    
    @abstractmethod
    def generate_signal(self, market_context: MarketContext) -> Optional[TradingSignal]:
        """
        Generate trading signal based on market context
        
        Args:
            market_context: Current market data and indicators
            
        Returns:
            TradingSignal or None if no signal
        """
        pass
    
    @abstractmethod
    def validate_signal(self, signal: TradingSignal, market_context: MarketContext) -> bool:
        """
        Validate a trading signal before execution
        
        Args:
            signal: Generated trading signal
            market_context: Current market context
            
        Returns:
            True if signal is valid
        """
        pass
    
    def update_parameters(self, new_parameters: Dict[str, Any]):
        """Update strategy parameters"""
        self.parameters.update(new_parameters)
        self.logger.info(f"Updated parameters for {self.name}: {new_parameters}")
    
    def get_parameter(self, key: str, default=None):
        """Get strategy parameter value"""
        return self.parameters.get(key, default)
    
    def set_parameter(self, key: str, value: Any):
        """Set strategy parameter value"""
        self.parameters[key] = value
        self.logger.debug(f"Set parameter {key}={value} for {self.name}")
    
    def enable(self):
        """Enable strategy"""
        self.active = True
        self.logger.info(f"Strategy {self.name} enabled")
    
    def disable(self):
        """Disable strategy"""
        self.active = False
        self.logger.info(f"Strategy {self.name} disabled")
    
    def is_active(self) -> bool:
        """Check if strategy is active"""
        return self.active
    
    def record_signal_result(self, success: bool):
        """Record the result of a signal execution"""
        self.performance_metrics['total_signals'] += 1
        if success:
            self.performance_metrics['successful_signals'] += 1
        
        # Update win rate
        total = self.performance_metrics['total_signals']
        successful = self.performance_metrics['successful_signals']
        self.performance_metrics['win_rate'] = (successful / total) * 100 if total > 0 else 0
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get strategy performance metrics"""
        return self.performance_metrics.copy()
    
    def reset_performance_metrics(self):
        """Reset performance tracking"""
        self.performance_metrics = {
            'total_signals': 0,
            'successful_signals': 0,
            'win_rate': 0.0
        }
        self.logger.info(f"Reset performance metrics for {self.name}")
    
    def calculate_position_size(self, signal: TradingSignal, account_balance: float, 
                              risk_per_trade: float = 0.01) -> float:
        """
        Calculate position size for a signal
        
        Args:
            signal: Trading signal
            account_balance: Available account balance
            risk_per_trade: Risk percentage per trade
            
        Returns:
            Calculated position size
        """
        try:
            # Basic position sizing based on risk percentage
            risk_amount = account_balance * risk_per_trade
            
            if signal.price and signal.stop_loss:
                # Calculate position size based on stop loss distance
                price_risk = abs(signal.price - signal.stop_loss)
                if price_risk > 0:
                    position_size = risk_amount / price_risk
                else:
                    position_size = risk_amount / (signal.price * 0.02)  # Default 2% risk
            else:
                # Default calculation
                position_size = risk_amount / (signal.price * 0.02) if signal.price else 0
            
            # Apply strategy-specific position sizing rules
            max_position = self.get_parameter('max_position_size', float('inf'))
            position_size = min(position_size, max_position)
            
            return max(0, position_size)
            
        except Exception as e:
            self.logger.error(f"Position size calculation error: {e}")
            return 0.0
    
    def should_exit_position(self, entry_price: float, current_price: float, 
                           side: str) -> Optional[str]:
        """
        Check if position should be exited based on strategy rules
        
        Args:
            entry_price: Entry price of position
            current_price: Current market price
            side: Position side (LONG/SHORT)
            
        Returns:
            Exit reason or None if should hold
        """
        try:
            # Basic stop loss and take profit check
            stop_loss_pct = self.get_parameter('stop_loss_pct', 0.02)
            take_profit_pct = self.get_parameter('take_profit_pct', 0.04)
            
            if side == "LONG":
                pnl_pct = (current_price - entry_price) / entry_price
            else:
                pnl_pct = (entry_price - current_price) / entry_price
            
            if pnl_pct <= -stop_loss_pct:
                return "STOP_LOSS"
            elif pnl_pct >= take_profit_pct:
                return "TAKE_PROFIT"
            
            return None
            
        except Exception as e:
            self.logger.error(f"Exit condition check error: {e}")
            return None
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get comprehensive strategy information"""
        return {
            'name': self.name,
            'active': self.active,
            'parameters': self.parameters,
            'performance': self.performance_metrics
        }
    
    def __str__(self) -> str:
        return f"{self.name} (Active: {self.active})"
    
    def __repr__(self) -> str:
        return f"Strategy(name='{self.name}', active={self.active}, parameters={self.parameters})"


class StrategyManager(LoggerMixin):
    """Manager for multiple trading strategies"""
    
    def __init__(self):
        self.strategies: Dict[str, BaseStrategy] = {}
        self.active_strategies: List[str] = []
    
    def add_strategy(self, strategy: BaseStrategy):
        """Add a strategy to the manager"""
        self.strategies[strategy.name] = strategy
        if strategy.is_active():
            self.active_strategies.append(strategy.name)
        self.logger.info(f"Added strategy: {strategy.name}")
    
    def remove_strategy(self, strategy_name: str):
        """Remove a strategy from the manager"""
        if strategy_name in self.strategies:
            del self.strategies[strategy_name]
            if strategy_name in self.active_strategies:
                self.active_strategies.remove(strategy_name)
            self.logger.info(f"Removed strategy: {strategy_name}")
    
    def enable_strategy(self, strategy_name: str):
        """Enable a specific strategy"""
        if strategy_name in self.strategies:
            self.strategies[strategy_name].enable()
            if strategy_name not in self.active_strategies:
                self.active_strategies.append(strategy_name)
    
    def disable_strategy(self, strategy_name: str):
        """Disable a specific strategy"""
        if strategy_name in self.strategies:
            self.strategies[strategy_name].disable()
            if strategy_name in self.active_strategies:
                self.active_strategies.remove(strategy_name)
    
    def generate_signals(self, market_context: MarketContext) -> List[TradingSignal]:
        """Generate signals from all active strategies"""
        signals = []
        
        for strategy_name in self.active_strategies:
            strategy = self.strategies[strategy_name]
            try:
                signal = strategy.generate_signal(market_context)
                if signal and strategy.validate_signal(signal, market_context):
                    signals.append(signal)
            except Exception as e:
                self.logger.error(f"Error generating signal from {strategy_name}: {e}")
        
        return signals
    
    def get_strategy_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics for all strategies"""
        return {
            name: strategy.get_performance_metrics()
            for name, strategy in self.strategies.items()
        }
    
    def get_active_strategies(self) -> List[str]:
        """Get list of active strategy names"""
        return self.active_strategies.copy()
    
    def get_all_strategies(self) -> Dict[str, BaseStrategy]:
        """Get all strategies"""
        return self.strategies.copy()