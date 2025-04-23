#!/usr/bin/env python3

import pcbnew
import os

def add_srm_mounting_holes():
    print("Adding SRM mounting holes for microBTX conversion...")
    
    # Load the PCB file
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    # microBTX SRM mounting hole positions (in mm from origin)
    # Based on BTX specification for SRM mounting
    srm_hole_positions_mm = [
        (115.00, 118.50),  # SRM Top Left
        (115.00, 148.50),  # SRM Bottom Left
        (145.00, 118.50),  # SRM Top Right
        (145.00, 148.50),  # SRM Bottom Right
    ]
    
    # Create SRM mounting holes
    holes_created = 0
    for i, (x_mm, y_mm) in enumerate(srm_hole_positions_mm):
        # Convert mm to KiCad internal units
        x_iu = int(x_mm * 1000000)
        y_iu = int(y_mm * 1000000)
        
        try:
            # Load mounting hole footprint
            hole = pcbnew.FootprintLoad("/usr/share/kicad/footprints/MountingHole.pretty", "MountingHole_3.2mm_M3")
            
            if hole:
                # Set position and reference
                hole.SetPosition(pcbnew.VECTOR2I(x_iu, y_iu))
                hole.SetReference(f"HSRM{i+1}")
                
                # Add to board
                board.Add(hole)
                holes_created += 1
            else:
                print(f"Warning: Could not create SRM mounting hole at position {x_mm:.2f}, {y_mm:.2f}")
        except Exception as e:
            print(f"Error creating SRM mounting hole: {e}")
    
    print(f"Created {holes_created} new SRM mounting holes")
    
    # Save modified board
    board.Save(pcb_file)
    print(f"Saved modified PCB to: {pcb_file}")
    
    return True

if __name__ == "__main__":
    success = add_srm_mounting_holes()
    if success:
        print("SRM mounting holes added successfully")
    else:
        print("Failed to add SRM mounting holes")
