"""
Mean reversion trading strategy for CryptoFuturesBot
Generates signals based on price mean reversion patterns
"""

from typing import Optional, List
import numpy as np

from .base_strategy import BaseStrategy, TradingSignal, MarketContext, SignalType

class MeanReversionStrategy(BaseStrategy):
    """Mean reversion trading strategy"""
    
    def __init__(self, parameters: Optional[dict] = None):
        """
        Initialize mean reversion strategy
        
        Args:
            parameters: Strategy parameters
        """
        default_params = {
            'lookback_period': 20,
            'std_dev_threshold': 2.0,
            'mean_reversion_period': 10,
            'stop_loss_pct': 0.015,
            'take_profit_pct': 0.03,
            'min_volume': 1000,
            'confidence_threshold': 0.7
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__("MeanReversion", default_params)
    
    def generate_signal(self, market_context: MarketContext) -> Optional[TradingSignal]:
        """
        Generate trading signal based on mean reversion
        
        Args:
            market_context: Current market data
            
        Returns:
            TradingSignal or None
        """
        try:
            if not self.is_active():
                return None
            
            lookback_period = self.get_parameter('lookback_period')
            
            # Check if we have enough data
            if len(market_context.price_history) < lookback_period:
                self.logger.debug(f"Insufficient price history for {market_context.symbol}")
                return None
            
            # Check minimum volume requirement
            if market_context.volume < self.get_parameter('min_volume'):
                return None
            
            # Calculate indicators
            indicators = self._calculate_indicators(market_context.price_history)
            
            # Generate signal based on mean reversion
            signal_type, confidence, reason = self._evaluate_mean_reversion(
                market_context.current_price, indicators
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
            self.logger.error(f"Error generating mean reversion signal: {e}")
            return None
    
    def _calculate_indicators(self, price_history: List[float]) -> dict:
        """Calculate mean reversion indicators"""
        try:
            prices = np.array(price_history)
            lookback_period = self.get_parameter('lookback_period')
            
            # Use the last lookback_period prices
            recent_prices = prices[-lookback_period:]
            
            # Calculate moving average and standard deviation
            mean_price = np.mean(recent_prices)
            std_dev = np.std(recent_prices)
            
            current_price = prices[-1]
            
            # Calculate Z-score (how many standard deviations from mean)
            z_score = (current_price - mean_price) / std_dev if std_dev > 0 else 0
            
            # Calculate price position relative to bollinger bands
            upper_band = mean_price + (2 * std_dev)
            lower_band = mean_price - (2 * std_dev)
            
            # Calculate momentum to confirm mean reversion
            momentum_period = min(10, len(prices) - 1)
            momentum = (prices[-1] - prices[-momentum_period]) / prices[-momentum_period]
            
            # Recent price volatility
            volatility = std_dev / mean_price if mean_price > 0 else 0
            
            return {
                'mean_price': mean_price,
                'std_dev': std_dev,
                'z_score': z_score,
                'upper_band': upper_band,
                'lower_band': lower_band,
                'current_price': current_price,
                'momentum': momentum,
                'volatility': volatility,
                'oversold': z_score < -self.get_parameter('std_dev_threshold'),
                'overbought': z_score > self.get_parameter('std_dev_threshold')
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating mean reversion indicators: {e}")
            return {}
    
    def _evaluate_mean_reversion(self, current_price: float, indicators: dict) -> tuple:
        """Evaluate mean reversion conditions"""
        try:
            z_score = indicators.get('z_score', 0)
            momentum = indicators.get('momentum', 0)
            volatility = indicators.get('volatility', 0)
            
            confidence = 0.0
            reason = ""
            signal_type = SignalType.HOLD
            
            # Mean reversion conditions
            oversold = indicators.get('oversold', False)
            overbought = indicators.get('overbought', False)
            
            # Look for mean reversion opportunities
            if oversold and momentum < 0:
                # Price is oversold and still declining - potential reversal
                signal_type = SignalType.BUY
                confidence = min(0.9, 0.5 + abs(z_score) * 0.1)
                reason = f"Oversold condition (Z-score: {z_score:.2f}) with negative momentum"
                
            elif overbought and momentum > 0:
                # Price is overbought and still rising - potential reversal
                signal_type = SignalType.SELL
                confidence = min(0.9, 0.5 + abs(z_score) * 0.1)
                reason = f"Overbought condition (Z-score: {z_score:.2f}) with positive momentum"
            
            # Adjust confidence based on volatility
            if volatility > 0.05:  # High volatility reduces confidence
                confidence *= 0.8
            elif volatility < 0.02:  # Low volatility increases confidence
                confidence *= 1.1
            
            # Ensure confidence doesn't exceed 1.0
            confidence = min(confidence, 1.0)
            
            return signal_type, confidence, reason
            
        except Exception as e:
            self.logger.error(f"Error evaluating mean reversion: {e}")
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
                if price_change > 0.005:  # 0.5% price change threshold for mean reversion
                    self.logger.warning(f"Price moved too much since signal generation: {price_change:.3%}")
                    return False
            
            # Check volume requirements
            if market_context.volume < self.get_parameter('min_volume'):
                return False
            
            # Additional validation for mean reversion strategy
            # Ensure we're not in a strong trending market
            if len(market_context.price_history) >= 20:
                recent_prices = market_context.price_history[-20:]
                trend_strength = abs(recent_prices[-1] - recent_prices[0]) / recent_prices[0]
                
                if trend_strength > 0.1:  # 10% move in 20 periods indicates strong trend
                    self.logger.warning(f"Strong trend detected, skipping mean reversion signal: {trend_strength:.2%}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating signal: {e}")
            return False