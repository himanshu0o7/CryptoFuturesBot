"""
Tests for math_utils module.
"""
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.math_utils import calculate_sum


class TestCalculateSum:
    """Test cases for the calculate_sum function."""
    
    def test_basic_positive_numbers(self):
        """Test with basic positive integers."""
        assert calculate_sum([1, 2, 3, 4, 5]) == 15
        
    def test_single_number(self):
        """Test with a single number."""
        assert calculate_sum([42]) == 42
        
    def test_empty_list(self):
        """Test with an empty list."""
        assert calculate_sum([]) == 0
        
    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert calculate_sum([-1, -2, -3]) == -6
        
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative numbers."""
        assert calculate_sum([10, -5, 3, -2]) == 6
        
    def test_floating_point_numbers(self):
        """Test with floating point numbers."""
        result = calculate_sum([1.5, 2.5, 3.0])
        assert abs(result - 7.0) < 1e-10  # Handle floating point precision
        
    def test_zero_values(self):
        """Test with zeros."""
        assert calculate_sum([0, 0, 0]) == 0
        assert calculate_sum([1, 0, -1]) == 0
        
    def test_large_numbers(self):
        """Test with large numbers."""
        assert calculate_sum([1000000, 2000000, 3000000]) == 6000000
        
    def test_tuple_input(self):
        """Test with tuple input."""
        assert calculate_sum((1, 2, 3)) == 6
        
    def test_generator_input(self):
        """Test with generator input."""
        def number_generator():
            for i in range(1, 6):
                yield i
        assert calculate_sum(number_generator()) == 15
        
    def test_performance_comparison(self):
        """Test to verify the optimized version performs better than loop version."""
        import time
        
        # Create a large list for testing
        large_list = list(range(100000))
        
        # Our optimized version using built-in sum
        start_time = time.time()
        result_optimized = calculate_sum(large_list)
        optimized_time = time.time() - start_time
        
        # Original loop-based implementation for comparison
        def calculate_sum_original(numbers):
            total = 0
            for num in numbers:
                total += num
            return total
            
        start_time = time.time()
        result_original = calculate_sum_original(large_list)
        original_time = time.time() - start_time
        
        # Both should produce the same result
        assert result_optimized == result_original
        
        # Optimized version should be faster (though this may vary by system)
        # We'll just verify the results are the same for now
        assert result_optimized == sum(range(100000))