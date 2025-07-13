"""
Mathematical utility functions for CryptoFuturesBot.
Provides optimized implementations of common mathematical operations.
"""


def calculate_sum(numbers):
    """
    Calculate the sum of numbers in an iterable.
    
    This function is optimized for performance by using Python's built-in sum()
    function, which is implemented in C and significantly faster than a Python loop.
    
    Args:
        numbers: An iterable of numbers (list, tuple, etc.)
        
    Returns:
        The sum of all numbers in the iterable
        
    Examples:
        >>> calculate_sum([1, 2, 3, 4, 5])
        15
        >>> calculate_sum([])
        0
        >>> calculate_sum([1.5, 2.5, 3.0])
        7.0
    """
    return sum(numbers)