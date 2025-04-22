#!/usr/bin/env python3
"""
Simple script to check if the PCB file can be opened.
"""
import os
import sys

def main():
    """Main function to check if the PCB file can be opened."""
    # Get the absolute path to the PCB file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    pcb_path = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    
    print(f"Checking PCB file: {pcb_path}")
    
    try:
        # Check if the file exists
        if not os.path.exists(pcb_path):
            print(f"Error: PCB file not found at {pcb_path}")
            return 1
            
        # Try to open the file
        with open(pcb_path, 'r') as f:
            # Read the first few lines
            header = ''.join([f.readline() for _ in range(10)])
            print("PCB file header:")
            print(header)
            
        print("PCB file opened successfully")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
