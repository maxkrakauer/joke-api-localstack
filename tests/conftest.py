import os
import sys

# Project root directory (C:\joke-api-localstack)
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Ensure project root is on sys.path so "import src" works
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
