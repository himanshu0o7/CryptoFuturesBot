"""Tests for master_controller.py module."""

import sys
from io import StringIO
import os

# Add the parent directory to the path so we can import master_controller
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import master_controller


def test_main_function_exists():
    """Test that main function exists and is callable."""
    assert hasattr(master_controller, "main")
    assert callable(master_controller.main)


def test_main_function_output():
    """Test that main function produces expected output."""
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        master_controller.main()
        output = captured_output.getvalue().strip()
        assert output == "Master controller executed"
    finally:
        sys.stdout = old_stdout


def test_main_function_returns_none():
    """Test that main function returns None."""
    result = master_controller.main()
    assert result is None