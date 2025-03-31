import os
import sys
from pathlib import Path

# اضافه کردن مسیر src به PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))