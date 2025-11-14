# tests/conftest.py
import sys
from pathlib import Path

# tests/ -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# This is the inner package directory: WeatherWatcherTUI/
PKG_DIR = PROJECT_ROOT / "WeatherWatcherTUI"

# Ensure that directory is on sys.path so `import processing` etc. works
sys.path.insert(0, str(PKG_DIR))
