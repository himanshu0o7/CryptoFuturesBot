"""
Simple momentum trading strategy for CryptoFuturesBot
Generates signals based on price momentum and moving averages
"""

from typing import Optional, List
import numpy as np

from .base_strategy import BaseStrategy, TradingSignal, MarketContext, SignalType
from utils.logging_setup import LoggerMixin

class SimpleMomentumStrategy(BaseStrategy):
    """Simple momentum-based trading strategy"""
    
    def __init__(self, parameters: Optional[dict] = None):
        """
        Initialize momentum strategy
        
        Args:
            parameters: Strategy parameters
        """
        default_params = {
            'fast_ma_period': 10,
            'slow_ma_period': 30,
            'momentum_threshold': 0.02,  # 2% momentum threshold
            'stop_loss_pct': 0.02,
            'take_profit_pct': 0.04,
            'min_volume': 1000,
            'confidence_threshold': 0.6
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__("SimpleMomentum", default_params)
    
    def generate_signal(self, market_context: MarketContext) -> Optional[TradingSignal]:
        """
        Generate trading signal based on momentum
        
        Args:
            market_context: Current market data
            
        Returns:
            TradingSignal or None
        """
        try:
            if not self.is_active():
                return None
            
            # Check if we have enough data
            if len(market_context.price_history) < self.get_parameter('slow_ma_period'):
                self.logger.debug(f"Insufficient price history for {market_context.symbol}")
                return None
            
            # Check minimum volume requirement
            if market_context.volume < self.get_parameter('min_volume'):
                return None
            
            # Calculate indicators
            indicators = self._calculate_indicators(market_context.price_history)
            
            # Generate signal based on conditions
            signal_type, confidence, reason = self._evaluate_conditions(
                market_context.current_price, indicators, market_context
            )
            
            if signal_type == SignalType.HOLD:
                return None
            
            # Check confidence threshold
            if confidence < self.get_parameter('confidence_threshold'):
                return None
            
            # Calculate stop loss and take profit
            stop_loss, take_profit = self._calculate_levels(
                market_context.current_price, signal_type
            )
            
            signal = TradingSignal(
                symbol=market_context.symbol,
                signal_type=signal_type,
                confidence=confidence,
                price=market_context.current_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                reason=reason,
                timestamp=market_context.timestamp
            )
            
            self.logger.info(f"Generated {signal_type.value} signal for {market_context.symbol}: {reason}")
            return signal
            
        except Exception as e:
            self.logger.error(f"Error generating momentum signal: {e}")
            return None
    
    def _calculate_indicators(self, price_history: List[float]) -> dict:
        """Calculate technical indicators"""
        try:
            prices = np.array(price_history)
            
            fast_period = self.get_parameter('fast_ma_period')
            slow_period = self.get_parameter('slow_ma_period')
            
            # Moving averages
            fast_ma = np.mean(prices[-fast_period:])
            slow_ma = np.mean(prices[-slow_period:])
            
            # Momentum
            momentum_period = min(fast_period, len(prices) - 1)
            momentum = (prices[-1] - prices[-momentum_period]) / prices[-momentum_period]
            
            # Price position relative to moving averages
            current_price = prices[-1]
            price_above_fast_ma = current_price > fast_ma
            price_above_slow_ma = current_price > slow_ma
            
            # Moving average crossover
            ma_crossover_bullish = fast_ma > slow_ma
            
            # Volatility (standard deviation)
            volatility = np.std(prices[-fast_period:]) / np.mean(prices[-fast_period:])
            
            return {
                'fast_ma': fast_ma,
                'slow_ma': slow_ma,
                'momentum': momentum,
                'price_above_fast_ma': price_above_fast_ma,
                'price_above_slow_ma': price_above_slow_ma,
                'ma_crossover_bullish': ma_crossover_bullish,
                'volatility': volatility,
                'current_price': current_price
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating indicators: {e}")
            return {}
    
    def _evaluate_conditions(self, current_price: float, indicators: dict, 
                           market_context: MarketContext) -> tuple:
        """Evaluate trading conditions and return signal type, confidence, and reason"""
        try:
            momentum_threshold = self.get_parameter('momentum_threshold')
            momentum = indicators.get('momentum', 0)
            
            # Initialize confidence and reason
            confidence = 0.0
            reason = ""
            signal_type = SignalType.HOLD
            
            # Bullish conditions
            bullish_conditions = []
            bearish_conditions = []
            
            # Check momentum
            if momentum > momentum_threshold:
                bullish_conditions.append(f"Strong upward momentum: {momentum:.2%}")
            elif momentum < -momentum_threshold:
                bearish_conditions.append(f"Strong downward momentum: {momentum:.2%}")
            
            # Check moving average conditions
            if indicators.get('ma_crossover_bullish', False):
                if indicators.get('price_above_fast_ma', False):
                    bullish_conditions.append("Price above fast MA and fast MA > slow MA")
            else:
                if not indicators.get('price_above_fast_ma', True):
                    bearish_conditions.append("Price below fast MA and fast MA < slow MA")
            
            # Check price position
            if indicators.get('price_above_slow_ma', False):
                bullish_conditions.append("Price above slow MA")
            else:
                bearish_conditions.append("Price below slow MA")
            
            # Evaluate overall signal
            if len(bullish_conditions) >= 2:
                signal_type = SignalType.BUY
                confidence = min(0.9, 0.3 + (len(bullish_conditions) * 0.2))
                reason = "; ".join(bullish_conditions)
                
            elif len(bearish_conditions) >= 2:
                signal_type = SignalType.SELL
                confidence = min(0.9, 0.3 + (len(bearish_conditions) * 0.2))
                reason = "; ".join(bearish_conditions)
            
            # Adjust confidence based on volatility
            volatility = indicators.get('volatility', 0)
            if volatility > 0.05:  # High volatility
                confidence *= 0.8  # Reduce confidence in high volatility
            
            return signal_type, confidence, reason
            
        except Exception as e:
            self.logger.error(f"Error evaluating conditions: {e}")
            return SignalType.HOLD, 0.0, "Error in evaluation"
    
    def _calculate_levels(self, price: float, signal_type: SignalType) -> tuple:
        """Calculate stop loss and take profit levels"""
        try:
            stop_loss_pct = self.get_parameter('stop_loss_pct')
            take_profit_pct = self.get_parameter('take_profit_pct')
            
            if signal_type == SignalType.BUY:
                stop_loss = price * (1 - stop_loss_pct)
                take_profit = price * (1 + take_profit_pct)
            elif signal_type == SignalType.SELL:
                stop_loss = price * (1 + stop_loss_pct)
                take_profit = price * (1 - take_profit_pct)
            else:
                stop_loss = None
                take_profit = None
            
            return stop_loss, take_profit
            
        except Exception as e:
            self.logger.error(f"Error calculating levels: {e}")
            return None, None
    
    def validate_signal(self, signal: TradingSignal, market_context: MarketContext) -> bool:
        """
        Validate signal before execution
        
        Args:
            signal: Generated signal
            market_context: Current market context
            
        Returns:
            True if signal is valid
        """
        try:
            # Basic validation
            if not signal or signal.confidence <= 0:
                return False
            
            # Check if price hasn't moved too much since signal generation
            if signal.price and market_context.current_price:
                price_change = abs(market_context.current_price - signal.price) / signal.price
                if price_change > 0.01:  # 1% price change threshold
                    self.logger.warning(f"Price moved too much since signal generation: {price_change:.2%}")
                    return False
            
            # Check volume requirements
            if market_context.volume < self.get_parameter('min_volume'):
                return False
            
            # Additional strategy-specific validation can be added here
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating signal: {e}")
            return False
    
    def should_exit_position(self, entry_price: float, current_price: float, 
                           side: str) -> Optional[str]:
        """
        Enhanced exit logic for momentum strategy
        
        Args:
            entry_price: Entry price
            current_price: Current price
            side: Position side
            
        Returns:
            Exit reason or None
        """
        try:
            # Check basic stop loss and take profit
            basic_exit = super().should_exit_position(entry_price, current_price, side)
            if basic_exit:
                return basic_exit
            
            # Additional momentum-specific exit conditions
            # For example, exit if momentum reverses significantly
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error checking exit conditions: {e}")
            return None