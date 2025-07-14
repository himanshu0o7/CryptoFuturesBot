# Dead Code Detection for CryptoFuturesBot

This utility helps identify unused code, imports, and variables in the CryptoFuturesBot codebase using the `vulture` static analysis tool.

## Quick Start

```bash
# Install dependencies (if not already installed)
pip install vulture

# Run basic dead code detection
python detect_unused_code.py

# Generate a report file
python detect_unused_code.py --output dead_code_report.txt

# Check only unused imports with high confidence
python detect_unused_code.py --imports-only

# Adjust confidence level (higher = fewer false positives)
python detect_unused_code.py --confidence 80
```

## Usage Examples

### Basic Usage
```bash
# Default report with 60% confidence
python detect_unused_code.py
```

### High Confidence Imports Only
```bash
# Only show unused imports with 80%+ confidence
python detect_unused_code.py --imports-only
```

### Custom Exclusions
```bash
# Exclude additional patterns
python detect_unused_code.py --exclude "test_*,*demo*"
```

### Generate Whitelist
```bash
# Generate whitelist format for suppressing false positives
python detect_unused_code.py --whitelist --output vulture_whitelist.py
```

## What It Detects

- **Unused imports**: Import statements that are never referenced
- **Unused variables**: Variables that are assigned but never used
- **Unused functions**: Functions that are defined but never called
- **Unused classes**: Classes that are defined but never instantiated
- **Dead code**: Code blocks that are unreachable

## Understanding the Output

The tool shows confidence levels for each detection:

- **90-100%**: Very likely unused (safe to remove)
- **70-89%**: Probably unused (review carefully)
- **60-69%**: Possibly unused (manual verification needed)

## Default Exclusions

The following patterns are automatically excluded:
- `*venv*` - Virtual environment files
- `.*` - Hidden directories (.git, .pytest_cache, etc.)
- `*.zip` - Archive files
- `*build*`, `*dist*` - Build artifacts
- `*__pycache__*` - Python cache directories
- `*.pyc` - Compiled Python files

## Testing

Run the test suite to verify functionality:

```bash
python test_detect_unused_code.py
```

## Notes

- **False Positives**: The tool may report false positives for:
  - Dynamic imports (`importlib`, `__import__`)
  - Attributes accessed via `getattr()`
  - Code called from templates or configuration files
  - Testing fixtures and mock objects

- **Manual Review**: Always manually review results before removing code

- **Integration**: This tool can be integrated into CI/CD pipelines for automated code quality checks

## Sample Output

```
================================================================================
CryptoFuturesBot - Dead Code Detection Report
================================================================================
Project Root: /path/to/CryptoFuturesBot
Minimum Confidence: 75%
Excluded Patterns: *venv*, .*, *.zip, *build*, *dist*, *__pycache__*
================================================================================

UNUSED CODE DETECTED:
----------------------------------------
openai_knowledge_tool.py:16: unused variable 'num_results' (100% confidence)
part1_core/coinswitch_futures_cancel_one_utils.py:5: unused import 'quote_plus' (90% confidence)

STATISTICS:
----------------------------------------
Total Python files: 2853
Excluded files: 2748
Analyzed files: 105
```