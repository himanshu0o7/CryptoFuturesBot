"""
Trading strategies module for CryptoFuturesBot
Contains various trading strategies and signal generators
"""

from .base_strategy import BaseStrategy
from .simple_momentum import SimpleMomentumStrategy
from .mean_reversion import MeanReversionStrategy

__all__ = [
    'BaseStrategy',
    'SimpleMomentumStrategy',
    'MeanReversionStrategy'
]