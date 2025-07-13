"""
Plotting utilities for CryptoFuturesBot.

This module provides functions for creating various types of plots
for data visualization and analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union, Optional


def plot_graph(x: Union[List, np.ndarray], y: Union[List, np.ndarray], 
               title: Optional[str] = None, xlabel: Optional[str] = None, 
               ylabel: Optional[str] = None, figsize: tuple = (10, 6)) -> None:
    """
    Create a basic line plot of x vs y data.
    
    Args:
        x: X-axis data points
        y: Y-axis data points
        title: Optional title for the plot
        xlabel: Optional label for x-axis
        ylabel: Optional label for y-axis
        figsize: Figure size as (width, height) tuple
        
    Raises:
        ValueError: If x and y have different lengths
        TypeError: If x or y are not array-like
    """
    # Validate inputs
    if len(x) != len(y):
        raise ValueError(f"x and y must have the same length. Got {len(x)} and {len(y)}")
    
    if len(x) == 0:
        raise ValueError("x and y cannot be empty")
    
    # Create the plot
    plt.figure(figsize=figsize)
    plt.plot(x, y)
    
    # Set labels and title if provided
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Show the plot
    plt.show()


def plot_candlestick_data(timestamps: List, open_prices: List, high_prices: List, 
                         low_prices: List, close_prices: List, title: Optional[str] = None) -> None:
    """
    Create a simple candlestick-style plot using matplotlib.
    
    Note: For more advanced candlestick plots, consider using plotly as used
    in the dashboard components.
    
    Args:
        timestamps: List of timestamps or labels for x-axis
        open_prices: Opening prices
        high_prices: High prices
        low_prices: Low prices
        close_prices: Closing prices
        title: Optional title for the plot
    """
    plt.figure(figsize=(12, 6))
    
    # Plot high-low lines
    for i, (ts, high, low) in enumerate(zip(timestamps, high_prices, low_prices)):
        plt.plot([i, i], [low, high], color='black', linewidth=1)
    
    # Plot open-close boxes (simplified)
    for i, (open_price, close_price) in enumerate(zip(open_prices, close_prices)):
        color = 'green' if close_price > open_price else 'red'
        plt.plot([i, i], [open_price, close_price], color=color, linewidth=3)
    
    if title:
        plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_price_history(prices: List[float], timestamps: Optional[List] = None, 
                      title: str = "Price History") -> None:
    """
    Plot price history over time.
    
    Args:
        prices: List of price values
        timestamps: Optional timestamps (if None, uses indices)
        title: Title for the plot
    """
    x_data = timestamps if timestamps is not None else range(len(prices))
    plot_graph(x_data, prices, title=title, xlabel="Time", ylabel="Price")