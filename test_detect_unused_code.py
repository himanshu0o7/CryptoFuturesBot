#!/usr/bin/env python3
"""
Test suite for the dead code detection utility.

This test verifies that the detect_unused_code.py script works correctly
and can detect unused code in test scenarios.
"""

import os
import tempfile
import unittest
from pathlib import Path
import sys

# Add the project root to the path to import our modules
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from detect_unused_code import DeadCodeDetector


class TestDeadCodeDetector(unittest.TestCase):
    """Test cases for the DeadCodeDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.detector = DeadCodeDetector(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_detector_initialization(self):
        """Test that the detector initializes correctly."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(str(self.detector.project_root), self.test_dir)
        self.assertIsInstance(self.detector.exclude_patterns, list)
        self.assertTrue(len(self.detector.exclude_patterns) > 0)
    
    def test_unused_import_detection(self):
        """Test detection of unused imports with a test file."""
        # Create a test Python file with unused imports
        test_file = Path(self.test_dir) / "test_unused.py"
        test_content = '''
import os  # This will be unused
import sys  # This will be used

def main():
    print(sys.version)
    return "hello"

if __name__ == "__main__":
    main()
'''
        test_file.write_text(test_content.strip())
        
        # Run detection
        result = self.detector.detect_unused_code(confidence=80)
        
        # Should detect unused 'os' import
        self.assertIn("unused import 'os'", result)
        # Should not complain about sys since it's used
        self.assertNotIn("unused import 'sys'", result)
    
    def test_unused_variable_detection(self):
        """Test detection of unused variables."""
        test_file = Path(self.test_dir) / "test_variables.py"
        test_content = '''
def example_function():
    used_var = "this is used"
    unused_var = "this is not used"  # Should be detected
    
    return used_var
'''
        test_file.write_text(test_content.strip())
        
        result = self.detector.detect_unused_code(confidence=60)
        
        # Should detect unused variable
        self.assertIn("unused_var", result)
    
    def test_exclude_patterns(self):
        """Test that exclude patterns work correctly."""
        # Create a venv directory with Python files
        venv_dir = Path(self.test_dir) / "venv" / "lib"
        venv_dir.mkdir(parents=True)
        
        venv_file = venv_dir / "some_lib.py"
        venv_file.write_text("import unused_import")
        
        # Create a regular project file
        project_file = Path(self.test_dir) / "project.py"
        project_file.write_text("import another_unused")
        
        result = self.detector.detect_unused_code(confidence=80)
        
        # Should not include venv files due to exclude patterns
        self.assertNotIn("venv", result)
        # But should include project files
        self.assertIn("project.py", result)
    
    def test_report_generation(self):
        """Test full report generation."""
        # Create a simple test file
        test_file = Path(self.test_dir) / "simple.py"
        test_file.write_text("import unused_module")
        
        report = self.detector.generate_report(confidence=80)
        
        # Check report structure
        self.assertIn("Dead Code Detection Report", report)
        self.assertIn("Project Root:", report)
        self.assertIn("STATISTICS:", report)
        self.assertIn("Total Python files:", report)
    
    def test_real_project_integration(self):
        """Test the detector on the actual project (integration test)."""
        # Use the real project directory
        real_detector = DeadCodeDetector(project_root)
        
        # This should run without errors
        result = real_detector.detect_unused_code(confidence=90)
        
        # Result should be a string (even if empty)
        self.assertIsInstance(result, str)
        
        # Should not contain venv paths
        self.assertNotIn("/venv/", result)


class TestScriptExecution(unittest.TestCase):
    """Test the script execution functionality."""
    
    def test_script_help(self):
        """Test that the script shows help without errors."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, "detect_unused_code.py", "--help"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Dead Code Detection", result.stdout)
    
    def test_script_confidence_validation(self):
        """Test that invalid confidence levels are rejected."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, "detect_unused_code.py", "--confidence", "150"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        self.assertNotEqual(result.returncode, 0)
        # Check either stderr or stdout for the error message
        error_output = (result.stderr + result.stdout).lower()
        self.assertIn("confidence level must be between", error_output)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)