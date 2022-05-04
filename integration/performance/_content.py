# Adds integraion to sys.path.

import os
import sys

libs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if libs not in sys.path:
    sys.path.append(libs)
