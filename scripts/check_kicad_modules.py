#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    """Check for KiCad Python modules."""
    print(f"Python version: {sys.version}")
    
    # Check for KiCad installation
    try:
        result = subprocess.run(["dpkg", "-l", "kicad"], capture_output=True, text=True)
        print(f"KiCad installation status:\n{result.stdout}")
    except Exception as e:
        print(f"Error checking KiCad installation: {e}")
    
    # Check for pcbnew module in system paths
    try:
        result = subprocess.run(["find", "/usr", "-name", "pcbnew.py"], capture_output=True, text=True)
        print(f"pcbnew.py locations:\n{result.stdout}")
    except Exception as e:
        print(f"Error finding pcbnew.py: {e}")
    
    # Check for _pcbnew module
    try:
        result = subprocess.run(["find", "/usr", "-name", "_pcbnew.so"], capture_output=True, text=True)
        print(f"_pcbnew.so locations:\n{result.stdout}")
    except Exception as e:
        print(f"Error finding _pcbnew.so: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
