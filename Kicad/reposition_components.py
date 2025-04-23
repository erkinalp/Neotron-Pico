import pcbnew
import os
import math

def reposition_components():
    print("Repositioning components to stay within board outline...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    backup_file = "neotron-pico-btx.kicad_pcb.reposition_backup"
    if not os.path.exists(backup_file):
        os.system(f"cp {pcb_file} {backup_file}")
        print(f"Created backup: {backup_file}")
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    board_bbox = board.GetBoardEdgesBoundingBox()
    board_min_x = board_bbox.GetX()
    board_min_y = board_bbox.GetY()
    board_width = board_bbox.GetWidth()
    board_height = board_bbox.GetHeight()
    board_max_x = board_min_x + board_width
    board_max_y = board_min_y + board_height
    
    print(f"Board dimensions: {board_width / 1000000.0:.2f} mm x {board_height / 1000000.0:.2f} mm")
    print(f"Board bounds: ({board_min_x / 1000000.0:.2f}, {board_min_y / 1000000.0:.2f}) to ({board_max_x / 1000000.0:.2f}, {board_max_y / 1000000.0:.2f})")
    
    srm_min_x = board_min_x + 102050000  # 102.05 mm from left edge
    srm_min_y = board_min_y + 103550000  # 103.55 mm from top edge
    srm_width = 60000000  # 60 mm
    srm_height = 60000000  # 60 mm
    srm_max_x = srm_min_x + srm_width
    srm_max_y = srm_min_y + srm_height
    
    print(f"SRM region: ({srm_min_x / 1000000.0:.2f}, {srm_min_y / 1000000.0:.2f}) to ({srm_max_x / 1000000.0:.2f}, {srm_max_y / 1000000.0:.2f})")
    
    category_a = []  # Non-mirrorable components (multi-pin ICs, processors, expansion slots)
    category_b = []  # Mirrorable components (passive components, two/three-terminal components)
    category_c = []  # Position-critical components (external connectors, mounting holes)
    
    outside_footprints = []
    heat_generating_components = []
    
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        fp_bbox = fp.GetBoundingBox()
        fp_min_x = fp_bbox.GetX()
        fp_min_y = fp_bbox.GetY()
        fp_width = fp_bbox.GetWidth()
        fp_height = fp_bbox.GetHeight()
        fp_max_x = fp_min_x + fp_width
        fp_max_y = fp_min_y + fp_height
        fp_center_x = fp_min_x + fp_width / 2
        fp_center_y = fp_min_y + fp_height / 2
        
        if ref.startswith('U') or ref.startswith('IC') or ref.startswith('CPU') or ref.startswith('MCU'):
            category_a.append(ref)
            heat_generating_components.append(ref)
        elif ref.startswith('R') or ref.startswith('C') or ref.startswith('L'):
            category_b.append(ref)
        elif ref.startswith('J') or ref.startswith('P') or ref.startswith('H'):
            category_c.append(ref)
        
        if (fp_min_x < board_min_x or fp_min_y < board_min_y or 
            fp_max_x > board_max_x or fp_max_y > board_max_y):
            outside_footprints.append((ref, fp_min_x, fp_min_y, fp_max_x, fp_max_y, fp_center_x, fp_center_y))
    
    print(f"\nComponent categorization:")
    print(f"Category A (Non-mirrorable): {len(category_a)} components")
    print(f"Category B (Mirrorable): {len(category_b)} components")
    print(f"Category C (Position-critical): {len(category_c)} components")
    
    if outside_footprints:
        print(f"\nFootprints outside board outline: {len(outside_footprints)}")
        
        components_repositioned = 0
        for ref, fp_min_x, fp_min_y, fp_max_x, fp_max_y, fp_center_x, fp_center_y in outside_footprints:
            fp = board.FindFootprintByReference(ref)
            if fp:
                current_pos = fp.GetPosition()
                current_x = current_pos.x
                current_y = current_pos.y
                
                new_x = current_x
                new_y = current_y
                
                if fp_min_x < board_min_x:
                    offset = board_min_x - fp_min_x + 5000000  # Add 5mm margin
                    new_x = current_x + offset
                
                if fp_max_x > board_max_x:
                    offset = fp_max_x - board_max_x + 5000000  # Add 5mm margin
                    new_x = current_x - offset
                
                if fp_min_y < board_min_y:
                    offset = board_min_y - fp_min_y + 5000000  # Add 5mm margin
                    new_y = current_y + offset
                
                if fp_max_y > board_max_y:
                    offset = fp_max_y - board_max_y + 5000000  # Add 5mm margin
                    new_y = current_y - offset
                
                new_pos = pcbnew.VECTOR2I(new_x, new_y)
                
                fp.SetPosition(new_pos)
                
                print(f"  Repositioned {ref} from ({current_x / 1000000.0:.2f}, {current_y / 1000000.0:.2f}) to ({new_x / 1000000.0:.2f}, {new_y / 1000000.0:.2f})")
                components_repositioned += 1
        
        print(f"Repositioned {components_repositioned} components")
    else:
        print("\nNo footprints outside board outline")
    
    heat_components_moved = 0
    for ref in heat_generating_components:
        fp = board.FindFootprintByReference(ref)
        if fp:
            fp_bbox = fp.GetBoundingBox()
            fp_center_x = fp_bbox.GetX() + fp_bbox.GetWidth() / 2
            fp_center_y = fp_bbox.GetY() + fp_bbox.GetHeight() / 2
            
            if (fp_center_x < srm_min_x or fp_center_x > srm_max_x or 
                fp_center_y < srm_min_y or fp_center_y > srm_max_y):
                
                srm_center_x = int(srm_min_x + srm_width / 2)
                srm_center_y = int(srm_min_y + srm_height / 2)
                
                current_pos = fp.GetPosition()
                
                new_pos = pcbnew.VECTOR2I(srm_center_x, srm_center_y)
                
                fp.SetPosition(new_pos)
                
                print(f"  Moved heat-generating component {ref} to SRM region")
                heat_components_moved += 1
    
    if heat_components_moved > 0:
        print(f"Moved {heat_components_moved} heat-generating components to SRM region")
    else:
        print("No heat-generating components needed to be moved to SRM region")
    
    pcbnew.SaveBoard(pcb_file, board)
    print(f"Saved modified PCB to {pcb_file}")
    
    return True

if __name__ == "__main__":
    reposition_components()
