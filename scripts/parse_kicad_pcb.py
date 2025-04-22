#!/usr/bin/env python3
"""
Script to parse and explore the KiCad PCB file structure.
This will help us understand how to modify the file directly.
"""
import os
import sys
import re
from pathlib import Path

def parse_pcb_file(pcb_path):
    """Parse the KiCad PCB file and extract key information."""
    try:
        with open(pcb_path, 'r') as f:
            content = f.read()
            
        print(f"Successfully read PCB file: {pcb_path}")
        print(f"File size: {len(content)} bytes")
        
        # Extract board outline information
        board_edges = re.findall(r'\(gr_line.*?\(layer "Edge\.Cuts"\).*?\)', content, re.DOTALL)
        print(f"Found {len(board_edges)} board edge segments")
        
        if board_edges:
            print("\nSample board edge segment:")
            print(board_edges[0])
        
        # Extract footprint information
        footprints = re.findall(r'\(footprint.*?\)\)', content, re.DOTALL)
        print(f"\nFound {len(footprints)} footprints")
        
        if footprints:
            print("\nSample footprint:")
            print(footprints[0][:500] + "..." if len(footprints[0]) > 500 else footprints[0])
        
        # Extract mounting hole information
        mounting_holes = [fp for fp in footprints if "MountingHole" in fp]
        print(f"\nFound {len(mounting_holes)} mounting holes")
        
        if mounting_holes:
            print("\nSample mounting hole:")
            print(mounting_holes[0])
        
        # Extract layer information
        layers = re.search(r'\(layers.*?\)', content, re.DOTALL)
        if layers:
            print("\nLayer stack:")
            print(layers.group(0))
        
        return {
            "board_edges": board_edges,
            "footprints": footprints,
            "mounting_holes": mounting_holes
        }
    except Exception as e:
        print(f"Error parsing PCB file: {e}")
        return None

def main():
    """Main function to parse and explore the KiCad PCB file."""
    # Get the absolute path to the PCB file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    pcb_path = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    
    # Parse the PCB file
    pcb_data = parse_pcb_file(pcb_path)
    
    if pcb_data:
        print("\nPCB file parsed successfully")
        
        # Create a backup of the PCB file
        backup_dir = os.path.join(repo_dir, "Kicad_Backup")
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, "neotron-pico.kicad_pcb.bak")
        
        with open(pcb_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
        
        print(f"\nBackup created at: {backup_path}")
        
        print("\nNext steps:")
        print("1. Create a script to mirror the board outline")
        print("2. Create a script to reposition components according to BTX specifications")
        print("3. Create a script to verify the conversion")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
