#!/usr/bin/env python3
import sys
print(f'Python version: {sys.version}')
print(f'Python path: {sys.path}')

try:
    import pcbnew
    print('pcbnew module available')
    print(f'pcbnew version: {pcbnew.GetBuildVersion()}')
except ImportError as e:
    print(f'pcbnew module not available: {e}')
