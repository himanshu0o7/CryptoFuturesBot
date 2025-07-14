#!/usr/bin/env python3
"""
Dead Code Detection Utility for CryptoFuturesBot

This script uses vulture to detect unused code, imports, and variables in the codebase.
It provides a comprehensive report of potentially dead code that can be reviewed and cleaned up.

Usage:
    python detect_unused_code.py [options]
    
Options:
    --confidence <int>  Set minimum confidence level (default: 60)
    --output <file>     Write results to file (default: stdout)
    --whitelist         Generate whitelist format output
    --sort-by-size      Sort results by code size
    --exclude <patterns> Exclude certain paths/patterns
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class DeadCodeDetector:
    """Utility class for detecting unused code using vulture."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.exclude_patterns = [
            "*venv*",           # Virtual environment
            ".*",               # Hidden directories (.git, .pytest_cache, etc.)
            "*.zip",            # Archive files  
            "*build*",          # Build artifacts
            "*dist*",           # Distribution artifacts
            "*__pycache__*",    # Python cache
            "*node_modules*",   # Node modules
            "*.pyc",            # Compiled Python files
        ]
    
    def detect_unused_code(
        self, 
        confidence: int = 60,
        exclude_additional: Optional[List[str]] = None,
        whitelist_mode: bool = False,
        sort_by_size: bool = False
    ) -> str:
        """
        Run vulture to detect unused code.
        
        Args:
            confidence: Minimum confidence level (0-100)
            exclude_additional: Additional patterns to exclude
            whitelist_mode: Generate whitelist format output
            sort_by_size: Sort results by code size
            
        Returns:
            String containing vulture output
        """
        cmd = ["vulture", str(self.project_root)]
        
        # Add confidence level
        cmd.extend(["--min-confidence", str(confidence)])
        
        # Add exclusions
        all_exclusions = self.exclude_patterns.copy()
        if exclude_additional:
            all_exclusions.extend(exclude_additional)
        if all_exclusions:
            cmd.extend(["--exclude", ",".join(all_exclusions)])
        
        # Add optional flags
        if whitelist_mode:
            cmd.append("--make-whitelist")
        if sort_by_size:
            cmd.append("--sort-by-size")
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=self.project_root
            )
            return result.stdout
        except FileNotFoundError:
            return "Error: vulture not found. Please install it: pip install vulture"
        except subprocess.SubprocessError as e:
            return f"Error running vulture: {e}"
    
    def detect_unused_imports(self, confidence: int = 80) -> str:
        """Specifically detect unused imports with higher confidence."""
        return self.detect_unused_code(confidence=confidence)
    
    def generate_report(self, confidence: int = 60, output_file: Optional[str] = None) -> str:
        """
        Generate a comprehensive dead code report.
        
        Args:
            confidence: Minimum confidence level
            output_file: File to write report to (optional)
            
        Returns:
            Report content as string
        """
        report_lines = [
            "=" * 80,
            "CryptoFuturesBot - Dead Code Detection Report",
            "=" * 80,
            f"Project Root: {self.project_root}",
            f"Minimum Confidence: {confidence}%",
            f"Excluded Patterns: {', '.join(self.exclude_patterns)}",
            "=" * 80,
            ""
        ]
        
        # Get unused code
        unused_code = self.detect_unused_code(confidence=confidence)
        if unused_code.strip():
            report_lines.extend([
                "UNUSED CODE DETECTED:",
                "-" * 40,
                unused_code,
                ""
            ])
        else:
            report_lines.extend([
                "✅ No unused code detected with current confidence level.",
                ""
            ])
        
        # Get high-confidence unused imports
        if confidence < 80:
            high_conf_imports = self.detect_unused_imports(confidence=80)
            if high_conf_imports.strip():
                report_lines.extend([
                    "HIGH-CONFIDENCE UNUSED IMPORTS (80%+):",
                    "-" * 40,
                    high_conf_imports,
                    ""
                ])
        
        # Statistics
        total_files = len(list(self.project_root.rglob("*.py")))
        excluded_files = len(list(self.project_root.rglob("venv/**/*.py")))
        analyzed_files = total_files - excluded_files
        
        report_lines.extend([
            "STATISTICS:",
            "-" * 40,
            f"Total Python files: {total_files}",
            f"Excluded files: {excluded_files}",
            f"Analyzed files: {analyzed_files}",
            ""
        ])
        
        report_lines.extend([
            "=" * 80,
            "Report completed. Review the results above.",
            "False positives may occur - manual review recommended.",
            "=" * 80
        ])
        
        report_content = "\n".join(report_lines)
        
        # Write to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_content)
                report_content += f"\n\nReport saved to: {output_file}"
            except IOError as e:
                report_content += f"\n\nError saving report: {e}"
        
        return report_content


def main():
    """Main entry point for the dead code detection utility."""
    parser = argparse.ArgumentParser(
        description="Detect unused code and imports in CryptoFuturesBot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--confidence", 
        type=int, 
        default=60,
        help="Minimum confidence level (0-100, default: 60)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Write report to file instead of stdout"
    )
    
    parser.add_argument(
        "--whitelist",
        action="store_true",
        help="Generate whitelist format output"
    )
    
    parser.add_argument(
        "--sort-by-size",
        action="store_true", 
        help="Sort results by code size"
    )
    
    parser.add_argument(
        "--exclude",
        type=str,
        help="Additional exclude patterns (comma-separated)"
    )
    
    parser.add_argument(
        "--imports-only",
        action="store_true",
        help="Only check for unused imports (confidence 80+)"
    )
    
    args = parser.parse_args()
    
    # Validate confidence level
    if not 0 <= args.confidence <= 100:
        print("Error: Confidence level must be between 0 and 100")
        sys.exit(1)
    
    # Initialize detector
    detector = DeadCodeDetector()
    
    # Handle different modes
    if args.imports_only:
        result = detector.detect_unused_imports(confidence=80)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"Unused imports report saved to: {args.output}")
        else:
            print(result)
    elif args.whitelist:
        exclude_additional = args.exclude.split(",") if args.exclude else None
        result = detector.detect_unused_code(
            confidence=args.confidence,
            exclude_additional=exclude_additional,
            whitelist_mode=True,
            sort_by_size=args.sort_by_size
        )
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"Whitelist saved to: {args.output}")
        else:
            print(result)
    else:
        # Generate full report
        report = detector.generate_report(
            confidence=args.confidence,
            output_file=args.output
        )
        if not args.output:
            print(report)


if __name__ == "__main__":
    main()