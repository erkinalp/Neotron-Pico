#!/usr/bin/env python3
"""
Script to open and explore the Neotron-Pico PCB file using KiCad's Python API.
"""
import sys
import os

def main():
    """Main function to open and explore the PCB file."""
    # Get the absolute path to the PCB file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    pcb_path = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    
    print(f"Opening PCB file: {pcb_path}")
    
    try:
        # Check if the file exists
        if not os.path.exists(pcb_path):
            print(f"Error: PCB file not found at {pcb_path}")
            return 1
            
        print(f"PCB file exists at {pcb_path}")
        print(f"File size: {os.path.getsize(pcb_path) / (1024 * 1024):.2f} MB")
        
        # We'll use pcbnew in a separate script after confirming it's installed
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
