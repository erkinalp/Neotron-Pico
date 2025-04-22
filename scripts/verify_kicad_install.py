#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    """Verify KiCad installation and pcbnew module availability."""
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check if KiCad is installed
    try:
        kicad_version = subprocess.check_output(["kicad", "--version"], stderr=subprocess.STDOUT, text=True)
        print(f"KiCad version: {kicad_version.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking KiCad version: {e.output}")
    except FileNotFoundError:
        print("KiCad executable not found in PATH")
    
    # Check for pcbnew module in system Python paths
    pcbnew_paths = []
    for path in sys.path:
        pcbnew_py = os.path.join(path, "pcbnew.py")
        if os.path.exists(pcbnew_py):
            pcbnew_paths.append(pcbnew_py)
    
    if pcbnew_paths:
        print(f"Found pcbnew.py at: {pcbnew_paths}")
    else:
        print("pcbnew.py not found in Python path")
    
    # Check for pcbnew module in system-wide locations
    try:
        pcbnew_system = subprocess.check_output(["find", "/usr", "-name", "pcbnew.py"], text=True)
        print(f"System pcbnew.py locations:\n{pcbnew_system}")
    except subprocess.CalledProcessError:
        print("Error searching for system pcbnew.py")
    
    # Try to import pcbnew using system Python
    try:
        # Add the directory containing pcbnew.py to Python path
        if pcbnew_paths:
            sys.path.insert(0, os.path.dirname(pcbnew_paths[0]))
        
        import pcbnew
        print(f"Successfully imported pcbnew module")
        print(f"pcbnew version: {pcbnew.GetBuildVersion()}")
        return True
    except ImportError as e:
        print(f"Failed to import pcbnew: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
