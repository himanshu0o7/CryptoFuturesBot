"""
Core module for CryptoFuturesBot.

This module contains the core functionality including utilities,
data handling, and business logic.
"""

from .utils import plot_graph, plot_price_history, plot_candlestick_data

__all__ = [
    'plot_graph',
    'plot_price_history', 
    'plot_candlestick_data'
]
