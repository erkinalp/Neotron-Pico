"""
Script to add SRM mounting holes to the Neotron-Pico BTX PCB.
This version uses VECTOR2I for positioning in KiCad 9.0.
"""
import pcbnew
import os
import sys

SRM_HOLES = [
    (190.0, 130.0),
    (190.0, 230.0),
    (250.0, 130.0),
    (250.0, 230.0)
]

def add_srm_mounting_holes(pcb_file):
    """Add SRM mounting holes to the PCB."""
    print(f"Adding SRM mounting holes to {pcb_file}...")
    
    backup_file = f"{pcb_file}.srm_holes_backup"
    if not os.path.exists(backup_file):
        os.system(f"cp {pcb_file} {backup_file}")
        print(f"Created backup: {backup_file}")
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    existing_holes = []
    for footprint in board.GetFootprints():
        ref = footprint.GetReference()
        if ref.startswith('H') and "MOUNT" in footprint.GetValue().upper():
            pos_x = footprint.GetPosition().x / 1000000.0
            pos_y = footprint.GetPosition().y / 1000000.0
            existing_holes.append((pos_x, pos_y))
    
    print(f"Found {len(existing_holes)} existing mounting holes")
    
    template_footprint = None
    for footprint in board.GetFootprints():
        if footprint.GetReference().startswith('H') and "MOUNT" in footprint.GetValue().upper():
            template_footprint = footprint
            break
    
    if template_footprint is None:
        print("Error: No existing mounting hole footprint found to use as template")
        return False
    
    holes_added = 0
    for i, (x_mm, y_mm) in enumerate(SRM_HOLES):
        hole_exists = False
        for ex_x, ex_y in existing_holes:
            if abs(ex_x - x_mm) <= 1.0 and abs(ex_y - y_mm) <= 1.0:
                hole_exists = True
                break
        
        if hole_exists:
            print(f"SRM mounting hole at ({x_mm:.2f}, {y_mm:.2f}) already exists")
            continue
        
        new_hole = pcbnew.FOOTPRINT(board)
        new_hole.SetReference(f"H{10+i}")
        new_hole.SetValue("MOUNT_HOLE_SRM")
        
        new_hole.SetLayer(template_footprint.GetLayer())
        new_hole.SetAttributes(template_footprint.GetAttributes())
        
        new_pad = pcbnew.PAD(new_hole)
        
        template_pad = None
        for pad in template_footprint.Pads():
            template_pad = pad
            break
        
        if template_pad:
            new_pad.SetShape(template_pad.GetShape())
            new_pad.SetSize(template_pad.GetSize())
            new_pad.SetDrillSize(template_pad.GetDrillSize())
            new_pad.SetLayerSet(template_pad.GetLayerSet())
            
            new_hole.Add(new_pad)
        
        x_iu = int(x_mm * 1000000)  # Convert mm to internal units
        y_iu = int(y_mm * 1000000)
        pos = pcbnew.VECTOR2I(x_iu, y_iu)
        new_hole.SetPosition(pos)
        
        board.Add(new_hole)
        
        print(f"Added SRM mounting hole at ({x_mm:.2f}, {y_mm:.2f})")
        holes_added += 1
    
    pcbnew.SaveBoard(pcb_file, board)
    print(f"Saved board to {pcb_file}")
    
    print(f"Added {holes_added} SRM mounting holes")
    return holes_added > 0

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 add_srm_holes_vector2i.py <pcb_file>")
        return 1
    
    pcb_file = sys.argv[1]
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return 1
    
    success = add_srm_mounting_holes(pcb_file)
    
    if success:
        print("SRM mounting holes added successfully")
        return 0
    else:
        print("Failed to add SRM mounting holes")
        return 1

if __name__ == "__main__":
    sys.exit(main())
