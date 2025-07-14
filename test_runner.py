"""
Test Runner for CryptoFuturesBot Modules
"""

import os
import sys
import logging
import importlib

# Setup logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Allowed parts
allowed_parts = [
    "part1_core",
    "part2_strategy",
    "part3_execution",
    "part4_monitoring",
    "part5_advanced",
    "shared_data",
    "template_modules",
]

# Validate arguments
if len(sys.argv) != 2:
    logging.error("Usage: python3 test_runner.py <part_name>")
    logging.info(f"Allowed parts: {allowed_parts}")
    sys.exit(1)

part_name = sys.argv[1]

if part_name not in allowed_parts:
    logging.error(f"Invalid part name: {part_name}")
    logging.info(f"Allowed parts: {allowed_parts}")
    sys.exit(1)

# Prepare module list
module_dir = os.path.join(os.getcwd(), part_name)

if not os.path.exists(module_dir):
    logging.error(f"Directory not found: {module_dir}")
    sys.exit(1)

module_files = [f for f in os.listdir(module_dir) if f.endswith(".py")]

if not module_files:
    logging.warning(f"No Python modules found in {module_dir}")
    sys.exit(0)

# Run each module
logging.info(f"Running modules in {part_name}...")

for module_file in module_files:
    module_path = f"{part_name}.{module_file[:-3]}"
    logging.info(f"Running module: {module_path}")

    try:
        mod = importlib.import_module(module_path)
        if hasattr(mod, "main"):
            mod.main()
        else:
            logging.warning(f"No main() function in {module_path}")
    except Exception as e:
        logging.error(f"Error running {module_path}: {e}")

logging.info("Test run completed.")
