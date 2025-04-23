import pcbnew
import os

def verify_srm_mounting_holes():
    print("Verifying SRM mounting holes...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    all_mounting_holes = []
    srm_mounting_holes = []
    
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('H'):
            pos = footprint.GetPosition()
            x_mm = pos.x / 1000000.0  # Convert from internal units to mm
            y_mm = pos.y / 1000000.0
            
            all_mounting_holes.append((ref, x_mm, y_mm))
            
            if ref.startswith('HSRM'):
                srm_mounting_holes.append((ref, x_mm, y_mm))
    
    print(f"Found {len(all_mounting_holes)} total mounting holes")
    print(f"Found {len(srm_mounting_holes)} SRM mounting holes")
    
    board_bbox = board.GetBoardEdgesBoundingBox()
    board_width_mm = board_bbox.GetWidth() / 1000000.0
    board_height_mm = board_bbox.GetHeight() / 1000000.0
    
    board_center_x = board_width_mm / 2
    board_center_y = board_height_mm / 2
    
    srm_width_mm = 60.0  # Approximate width of SRM region
    srm_height_mm = 60.0  # Approximate height of SRM region
    
    srm_left = board_center_x - (srm_width_mm / 2)
    srm_right = board_center_x + (srm_width_mm / 2)
    srm_top = board_center_y - (srm_height_mm / 2)
    srm_bottom = board_center_y + (srm_height_mm / 2)
    
    print(f"\nSRM Region Boundaries:")
    print(f"  Left: {srm_left:.2f} mm")
    print(f"  Right: {srm_right:.2f} mm")
    print(f"  Top: {srm_top:.2f} mm")
    print(f"  Bottom: {srm_bottom:.2f} mm")
    
    print("\nSRM Mounting Hole Positions:")
    for ref, x, y in srm_mounting_holes:
        in_srm_region = (srm_left <= x <= srm_right) and (srm_top <= y <= srm_bottom)
        status = "✓" if in_srm_region else "✗"
        print(f"  {status} {ref}: ({x:.2f} mm, {y:.2f} mm)")
    
    expected_srm_holes = 4
    if len(srm_mounting_holes) == expected_srm_holes:
        print(f"\n✓ Correct number of SRM mounting holes: {len(srm_mounting_holes)}")
    else:
        print(f"\n✗ Incorrect number of SRM mounting holes: {len(srm_mounting_holes)} (expected {expected_srm_holes})")
    
    srm_holes_in_region = all((srm_left <= x <= srm_right) and (srm_top <= y <= srm_bottom) for _, x, y in srm_mounting_holes)
    if srm_holes_in_region:
        print("✓ All SRM mounting holes are within the SRM region")
    else:
        print("✗ Some SRM mounting holes are outside the SRM region")
    
    return True

if __name__ == "__main__":
    verify_srm_mounting_holes()
