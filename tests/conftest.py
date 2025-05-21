# tests/conftest.py
"""
Pytest automatically imports this file before running any tests.
We push the repo root onto sys.path so `import app.*` works no
matter where pytest's working directory is.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # ../ (project root)
sys.path.insert(0, str(ROOT))