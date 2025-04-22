#!/usr/bin/env python3

import pcbnew
import os
import sys

def modify_pcb_layout():
    print("Starting PCB modification for microBTX conversion...")
    
    # Load the PCB file
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    # Get original board dimensions
    original_bbox = board.GetBoardEdgesBoundingBox()
    original_width_mm = original_bbox.GetWidth() / 1000000.0  # Convert from internal units to mm
    original_height_mm = original_bbox.GetHeight() / 1000000.0
    print(f"Original board dimensions: {original_width_mm:.2f} mm x {original_height_mm:.2f} mm")
    
    # microBTX dimensions (264mm x 267mm)
    target_width_mm = 264.0
    target_height_mm = 267.0
    
    # Create backup
    backup_file = f"{pcb_file}.backup"
    board.Save(backup_file)
    print(f"Created backup at: {backup_file}")
    
    # Modify board outline to match microBTX specifications
    print("Modifying board outline to match microBTX specifications...")
    
    # Find board outline segments
    board_outline_segments = []
    for drawing in board.GetDrawings():
        if drawing.GetClass() == "PCB_SHAPE" and drawing.GetLayer() == pcbnew.Edge_Cuts:
            board_outline_segments.append(drawing)
    
    if not board_outline_segments:
        print("Error: Could not find board outline segments")
        return False
    
    print(f"Found {len(board_outline_segments)} board outline segments")
    
    # Scale board outline
    for segment in board_outline_segments:
        # Remove old segment
        board.Remove(segment)
    
    # Create new board outline (simple rectangle for microBTX)
    new_outline = pcbnew.PCB_SHAPE(board)
    new_outline.SetLayer(pcbnew.Edge_Cuts)
    new_outline.SetShape(pcbnew.SHAPE_T_RECT)
    
    # Convert mm to KiCad internal units (nanometers)
    origin_x = 0
    origin_y = 0
    width_iu = int(target_width_mm * 1000000)
    height_iu = int(target_height_mm * 1000000)
    
    # Set rectangle points
    new_outline.SetStart(pcbnew.VECTOR2I(origin_x, origin_y))
    new_outline.SetEnd(pcbnew.VECTOR2I(origin_x + width_iu, origin_y + height_iu))
    
    # Add new outline to board
    board.Add(new_outline)
    print(f"Created new board outline: {target_width_mm:.2f} mm x {target_height_mm:.2f} mm")
    
    # Update mounting holes for microBTX
    print("Updating mounting holes for microBTX specification...")
    
    # microBTX mounting hole positions (in mm from origin)
    mounting_hole_positions_mm = [
        (6.35, 6.35),       # Bottom left
        (6.35, 260.65),     # Top left
        (257.65, 6.35),     # Bottom right
        (257.65, 260.65),   # Top right
        (130.0, 133.5)      # Center
    ]
    
    # Find existing mounting holes by reference designator
    mounting_holes = []
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('H'):
            mounting_holes.append(footprint)
    
    print(f"Found {len(mounting_holes)} existing mounting holes")
    
    # Remove existing mounting holes
    for hole in mounting_holes:
        board.Remove(hole)
    
    # Create new mounting holes at microBTX positions
    holes_created = 0
    for i, (x_mm, y_mm) in enumerate(mounting_hole_positions_mm):
        # Convert mm to KiCad internal units
        x_iu = int(x_mm * 1000000)
        y_iu = int(y_mm * 1000000)
        
        try:
            # Load mounting hole footprint
            hole = pcbnew.FootprintLoad("/usr/share/kicad/footprints/MountingHole.pretty", "MountingHole_3.2mm_M3")
            
            if hole:
                # Set position and reference
                hole.SetPosition(pcbnew.VECTOR2I(x_iu, y_iu))
                hole.SetReference(f"H{i+1}")
                
                # Add to board
                board.Add(hole)
                holes_created += 1
            else:
                print(f"Warning: Could not create mounting hole at position {x_mm:.2f}, {y_mm:.2f}")
        except Exception as e:
            print(f"Error creating mounting hole: {e}")
    
    print(f"Created {holes_created} new mounting holes for microBTX specification")
    
    # Save modified board
    board.Save(pcb_file)
    print(f"Saved modified PCB to: {pcb_file}")
    
    # Verify final dimensions
    final_board = pcbnew.LoadBoard(pcb_file)
    final_bbox = final_board.GetBoardEdgesBoundingBox()
    final_width_mm = final_bbox.GetWidth() / 1000000.0
    final_height_mm = final_bbox.GetHeight() / 1000000.0
    print(f"Final board dimensions: {final_width_mm:.2f} mm x {final_height_mm:.2f} mm")
    
    return True

if __name__ == "__main__":
    success = modify_pcb_layout()
    if success:
        print("microBTX conversion completed successfully")
    else:
        print("microBTX conversion failed")
        sys.exit(1)
