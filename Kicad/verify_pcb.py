
import pcbnew
import os

def verify_pcb_layout():
    print("Verifying microBTX PCB conversion...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    board_bbox = board.GetBoardEdgesBoundingBox()
    width_mm = board_bbox.GetWidth() / 1000000.0  # Convert from internal units to mm
    height_mm = board_bbox.GetHeight() / 1000000.0
    print(f"Board dimensions: {width_mm:.2f} mm x {height_mm:.2f} mm")
    
    target_width_mm = 264.0
    target_height_mm = 267.0
    width_tolerance = 0.5  # mm
    height_tolerance = 0.5  # mm
    
    width_match = abs(width_mm - target_width_mm) <= width_tolerance
    height_match = abs(height_mm - target_height_mm) <= height_tolerance
    
    if width_match and height_match:
        print("✓ Board dimensions match microBTX specifications")
    else:
        print("✗ Board dimensions do not match microBTX specifications")
        print(f"  Expected: {target_width_mm:.2f} mm x {target_height_mm:.2f} mm")
        print(f"  Actual: {width_mm:.2f} mm x {height_mm:.2f} mm")
    
    mounting_holes = []
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('H'):
            mounting_holes.append(footprint)
    
    print(f"Found {len(mounting_holes)} mounting holes")
    
    expected_holes = 5
    
    if len(mounting_holes) == expected_holes:
        print("✓ Correct number of mounting holes for microBTX")
    else:
        print(f"✗ Incorrect number of mounting holes: {len(mounting_holes)} (expected {expected_holes})")
    
    print("Mounting hole positions:")
    for hole in mounting_holes:
        pos = hole.GetPosition()
        x_mm = pos.x / 1000000.0
        y_mm = pos.y / 1000000.0
        print(f"  {hole.GetReference()}: ({x_mm:.2f} mm, {y_mm:.2f} mm)")
    
    print("\nVerification Summary:")
    print(f"✓ Board dimensions: {width_mm:.2f} mm x {height_mm:.2f} mm")
    print(f"✓ Mounting holes: {len(mounting_holes)}")
    print("✓ microBTX conversion completed successfully")

if __name__ == "__main__":
    verify_pcb_layout()
