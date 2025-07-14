"""
Example usage of the plot_graph function.

This script demonstrates how to use the plotting utilities
in the CryptoFuturesBot.
"""

import numpy as np
import matplotlib
# Use Agg backend for non-interactive environments
matplotlib.use('Agg')

from core.utils.plotting import plot_graph, plot_price_history


def demo_basic_plotting():
    """Demonstrate basic plotting functionality."""
    print("🔵 Demo: Basic line plot")
    
    # Simple linear data
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    
    plot_graph(x, y, title="Linear Growth", xlabel="Time", ylabel="Value")
    print("✅ Basic plot created successfully")


def demo_crypto_price_simulation():
    """Demonstrate plotting simulated crypto price data."""
    print("🔵 Demo: Crypto price simulation")
    
    # Simulate some price data
    np.random.seed(42)  # For reproducible results
    time_points = np.arange(0, 100, 1)
    base_price = 50000  # Starting price (e.g., BTC)
    
    # Create some realistic price movement
    price_changes = np.random.normal(0, 500, len(time_points))
    prices = [base_price]
    
    for change in price_changes[1:]:
        new_price = prices[-1] + change
        # Ensure price doesn't go negative
        new_price = max(new_price, 1000)
        prices.append(new_price)
    
    plot_price_history(prices, title="Simulated Crypto Price Movement")
    print("✅ Crypto price simulation plot created successfully")


def demo_numpy_arrays():
    """Demonstrate plotting with numpy arrays."""
    print("🔵 Demo: Numpy array plotting")
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * 1000 + 50000  # Sine wave around 50k (like BTC price oscillation)
    
    plot_graph(x, y, title="Oscillating Price Pattern", 
               xlabel="Time (hours)", ylabel="Price (USD)")
    print("✅ Numpy array plot created successfully")


if __name__ == "__main__":
    print("🚀 CryptoFuturesBot Plotting Demo")
    print("=" * 40)
    
    try:
        demo_basic_plotting()
        print()
        
        demo_crypto_price_simulation()
        print()
        
        demo_numpy_arrays()
        print()
        
        print("🎉 All plotting demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        raise