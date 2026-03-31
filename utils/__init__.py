import logging
import sys
from pathlib import Path

import yaml

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """Return a named logger with a consistent format. Safe to call multiple times."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
        logger.addHandler(handler)

    return logger


def load_test_data(test_file: str, test_name: str) -> list[dict]:
    """Load iteration data from a YAML file that matches the test file name.

    The YAML file must sit next to the test file and have the same stem.
    Example: tests/test_todo.py  →  tests/test_todo.yaml

    YAML structure:
        test_function_name:
          - {key: value, ...}
          - {key: value, ...}
    """
    yaml_path = Path(test_file).with_suffix(".yaml")
    if not yaml_path.exists():
        raise FileNotFoundError(f"Test data file not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    iterations = data.get(test_name, [])
    if not iterations:
        raise ValueError(f"No iterations found for '{test_name}' in {yaml_path}")

    return iterations
