"""
pytest configuration file
"""

import sys
from pathlib import Path

# Add the project root to the path so we can import our modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# pytest fixtures can be defined here