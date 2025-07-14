"""
Risk management utilities for CryptoFuturesBot
Handles stop-loss, take-profit, and position sizing
"""

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class RiskDecision(Enum):
    """Risk management decisions"""
    HOLD = "HOLD"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"
    PARTIAL_PROFIT = "PARTIAL_PROFIT"


@dataclass
class RiskLimits:
    """Risk management limits configuration"""
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.04  # 4% take profit
    max_position_size: float = 1000.0  # Maximum position size
    max_daily_loss: float = 500.0  # Maximum daily loss
    max_drawdown_pct: float = 0.10  # 10% maximum drawdown
    trailing_stop_pct: float = 0.015  # 1.5% trailing stop


class RiskManager:
    """Risk management system for trading operations"""
    
    def __init__(self, sl_pct: float = 0.02, tp_pct: float = 0.04, 
                 max_position_size: float = 1000.0):
        """
        Initialize risk manager
        
        Args:
            sl_pct: Stop loss percentage (0.02 = 2%)
            tp_pct: Take profit percentage (0.04 = 4%)
            max_position_size: Maximum position size
        """
        self.limits = RiskLimits(
            stop_loss_pct=sl_pct,
            take_profit_pct=tp_pct,
            max_position_size=max_position_size
        )
        self.daily_pnl = 0.0
        self.peak_value = 0.0
        self.logger = logging.getLogger(__name__)
    
    def should_exit(self, entry_price: float, current_price: float, 
                   side: str = "LONG") -> Optional[str]:
        """
        Determine if position should be exited
        
        Args:
            entry_price: Entry price of the position
            current_price: Current market price
            side: Position side (LONG/SHORT)
            
        Returns:
            Exit decision or None if should hold
        """
        if side.upper() == "LONG":
            pnl_pct = (current_price - entry_price) / entry_price
        else:  # SHORT
            pnl_pct = (entry_price - current_price) / entry_price
        
        # Check stop loss
        if pnl_pct <= -self.limits.stop_loss_pct:
            self.logger.warning(f"Stop loss triggered: {pnl_pct:.2%}")
            return RiskDecision.STOP_LOSS.value
        
        # Check take profit
        if pnl_pct >= self.limits.take_profit_pct:
            self.logger.info(f"Take profit triggered: {pnl_pct:.2%}")
            return RiskDecision.TAKE_PROFIT.value
        
        return None
    
    def calculate_position_size(self, account_balance: float, risk_per_trade: float = 0.01,
                              entry_price: float = 0.0, stop_loss_price: float = 0.0) -> float:
        """
        Calculate appropriate position size based on risk management
        
        Args:
            account_balance: Available account balance
            risk_per_trade: Risk percentage per trade (0.01 = 1%)
            entry_price: Planned entry price
            stop_loss_price: Planned stop loss price
            
        Returns:
            Calculated position size
        """
        # Risk amount per trade
        risk_amount = account_balance * risk_per_trade
        
        # If stop loss price is provided, calculate based on price difference
        if entry_price > 0 and stop_loss_price > 0:
            price_risk = abs(entry_price - stop_loss_price)
            if price_risk > 0:
                position_size = risk_amount / price_risk
            else:
                position_size = risk_amount / (entry_price * self.limits.stop_loss_pct)
        else:
            # Default calculation based on stop loss percentage
            position_size = risk_amount / (entry_price * self.limits.stop_loss_pct)
        
        # Apply maximum position size limit
        position_size = min(position_size, self.limits.max_position_size)
        
        # Ensure position size doesn't exceed account balance
        position_size = min(position_size, account_balance * 0.95)  # Keep 5% buffer
        
        self.logger.info(f"Calculated position size: {position_size:.2f}")
        return position_size
    
    def check_daily_limits(self, current_pnl: float) -> bool:
        """
        Check if daily loss limits are exceeded
        
        Args:
            current_pnl: Current day's PnL
            
        Returns:
            True if within limits, False if limits exceeded
        """
        self.daily_pnl = current_pnl
        
        if current_pnl <= -self.limits.max_daily_loss:
            self.logger.error(f"Daily loss limit exceeded: {current_pnl:.2f}")
            return False
        
        return True
    
    def check_drawdown(self, current_value: float) -> bool:
        """
        Check maximum drawdown limits
        
        Args:
            current_value: Current portfolio value
            
        Returns:
            True if within limits, False if limits exceeded
        """
        # Update peak value
        if current_value > self.peak_value:
            self.peak_value = current_value
        
        # Calculate drawdown
        if self.peak_value > 0:
            drawdown = (self.peak_value - current_value) / self.peak_value
            
            if drawdown >= self.limits.max_drawdown_pct:
                self.logger.error(f"Maximum drawdown exceeded: {drawdown:.2%}")
                return False
        
        return True
    
    def validate_trade(self, trade_params: Dict[str, Any]) -> bool:
        """
        Validate a trade against risk management rules
        
        Args:
            trade_params: Dictionary containing trade parameters
            
        Returns:
            True if trade is valid, False otherwise
        """
        try:
            symbol = trade_params.get('symbol', '')
            quantity = float(trade_params.get('quantity', 0))
            price = float(trade_params.get('price', 0))
            
            # Check position size
            position_value = quantity * price
            if position_value > self.limits.max_position_size:
                self.logger.warning(f"Position size too large: {position_value}")
                return False
            
            # Additional validation logic can be added here
            
            return True
            
        except (ValueError, KeyError) as e:
            self.logger.error(f"Trade validation error: {e}")
            return False
    
    def get_risk_metrics(self) -> Dict[str, Any]:
        """
        Get current risk metrics
        
        Returns:
            Dictionary of risk metrics
        """
        return {
            'stop_loss_pct': self.limits.stop_loss_pct,
            'take_profit_pct': self.limits.take_profit_pct,
            'max_position_size': self.limits.max_position_size,
            'daily_pnl': self.daily_pnl,
            'peak_value': self.peak_value,
            'max_daily_loss': self.limits.max_daily_loss,
            'max_drawdown_pct': self.limits.max_drawdown_pct
        }


class AdvancedRiskManager(RiskManager):
    """Advanced risk manager with additional features"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position_history = []
        self.volatility_factor = 1.0
    
    def calculate_dynamic_stop_loss(self, volatility: float, base_sl: float = None) -> float:
        """
        Calculate dynamic stop loss based on market volatility
        
        Args:
            volatility: Market volatility measure
            base_sl: Base stop loss percentage
            
        Returns:
            Adjusted stop loss percentage
        """
        if base_sl is None:
            base_sl = self.limits.stop_loss_pct
        
        # Adjust stop loss based on volatility
        # Higher volatility = wider stop loss
        volatility_multiplier = 1 + (volatility * 0.5)
        dynamic_sl = base_sl * volatility_multiplier
        
        # Cap the stop loss to reasonable limits
        dynamic_sl = min(dynamic_sl, base_sl * 2)  # Max 2x base SL
        dynamic_sl = max(dynamic_sl, base_sl * 0.5)  # Min 0.5x base SL
        
        self.logger.info(f"Dynamic stop loss calculated: {dynamic_sl:.2%}")
        return dynamic_sl
    
    def implement_trailing_stop(self, entry_price: float, current_price: float, 
                               highest_price: float, side: str = "LONG") -> Optional[float]:
        """
        Implement trailing stop loss
        
        Args:
            entry_price: Entry price
            current_price: Current market price
            highest_price: Highest price since entry
            side: Position side
            
        Returns:
            New stop loss price or None
        """
        if side.upper() == "LONG":
            # Calculate trailing stop price
            trailing_stop_price = highest_price * (1 - self.limits.trailing_stop_pct)
            
            # Only update if new stop is higher than entry-based stop
            entry_stop_price = entry_price * (1 - self.limits.stop_loss_pct)
            
            if trailing_stop_price > entry_stop_price:
                return trailing_stop_price
        
        return None