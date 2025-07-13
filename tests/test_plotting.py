"""
Tests for plotting utilities.
"""

import pytest
import numpy as np
import matplotlib
# Use non-interactive backend for testing
matplotlib.use('Agg')
from unittest.mock import patch

# Import the plotting functions
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.utils.plotting import plot_graph, plot_price_history


class TestPlotGraph:
    """Test cases for plot_graph function."""
    
    def test_plot_graph_basic(self):
        """Test basic functionality of plot_graph."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        
        # Mock plt.show to avoid displaying plot during tests
        with patch('matplotlib.pyplot.show'):
            plot_graph(x, y)
        
        # Test passes if no exception is raised
        assert True
    
    def test_plot_graph_with_numpy_arrays(self):
        """Test plot_graph with numpy arrays."""
        x = np.array([0, 1, 2, 3, 4])
        y = np.array([0, 1, 4, 9, 16])
        
        with patch('matplotlib.pyplot.show'):
            plot_graph(x, y, title="Squares", xlabel="Number", ylabel="Square")
        
        assert True
    
    def test_plot_graph_empty_data(self):
        """Test plot_graph with empty data."""
        x = []
        y = []
        
        with pytest.raises(ValueError, match="x and y cannot be empty"):
            plot_graph(x, y)
    
    def test_plot_graph_mismatched_lengths(self):
        """Test plot_graph with mismatched x and y lengths."""
        x = [1, 2, 3]
        y = [1, 2]
        
        with pytest.raises(ValueError, match="x and y must have the same length"):
            plot_graph(x, y)
    
    def test_plot_graph_single_point(self):
        """Test plot_graph with single data point."""
        x = [1]
        y = [1]
        
        with patch('matplotlib.pyplot.show'):
            plot_graph(x, y)
        
        assert True
    
    def test_plot_price_history(self):
        """Test plot_price_history function."""
        prices = [100.0, 105.5, 102.3, 108.7, 110.2]
        
        with patch('matplotlib.pyplot.show'):
            plot_price_history(prices)
        
        assert True
    
    def test_plot_price_history_with_timestamps(self):
        """Test plot_price_history with timestamps."""
        prices = [100.0, 105.5, 102.3]
        timestamps = ['2023-01-01', '2023-01-02', '2023-01-03']
        
        with patch('matplotlib.pyplot.show'):
            plot_price_history(prices, timestamps, title="BTC Price")
        
        assert True


if __name__ == "__main__":
    pytest.main([__file__])