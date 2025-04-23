import pcbnew
import math
import os

def check_srm_mounting_holes():
    print("Checking SRM mounting hole positions...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    srm_holes = []
    
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('HSRM'):
            pos = footprint.GetPosition()
            x_mm = pos.x / 1000000.0  # Convert from internal units to mm
            y_mm = pos.y / 1000000.0
            srm_holes.append((ref, x_mm, y_mm))
    
    srm_holes.sort()
    
    print(f"Found {len(srm_holes)} SRM mounting holes")
    
    print("\nSRM Mounting Hole Positions:")
    for ref, x, y in srm_holes:
        print(f"  {ref}: ({x:.2f} mm, {y:.2f} mm)")
    
    if len(srm_holes) >= 4:
        print("\nDistances between SRM mounting holes:")
        for i in range(len(srm_holes)):
            for j in range(i+1, len(srm_holes)):
                ref1, x1, y1 = srm_holes[i]
                ref2, x2, y2 = srm_holes[j]
                distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                print(f"  {ref1} to {ref2}: {distance:.2f} mm")
        
        if len(srm_holes) == 4:
            ref1, x1, y1 = srm_holes[0]  # HSRM1
            ref3, x3, y3 = srm_holes[2]  # HSRM3
            diagonal1 = math.sqrt((x3-x1)**2 + (y3-y1)**2)
            
            ref2, x2, y2 = srm_holes[1]  # HSRM2
            ref4, x4, y4 = srm_holes[3]  # HSRM4
            diagonal2 = math.sqrt((x4-x2)**2 + (y4-y2)**2)
            
            print(f"\nDiagonal distances:")
            print(f"  {ref1} to {ref3}: {diagonal1:.2f} mm")
            print(f"  {ref2} to {ref4}: {diagonal2:.2f} mm")
            
            tolerance = 0.1  # mm
            if abs(diagonal1 - diagonal2) <= tolerance:
                print("\n✓ SRM mounting holes form a perfect rectangle")
            else:
                print("\n✗ SRM mounting holes do not form a perfect rectangle")
                print(f"  Difference in diagonals: {abs(diagonal1 - diagonal2):.2f} mm")
        
        min_x = min(x for _, x, _ in srm_holes)
        max_x = max(x for _, x, _ in srm_holes)
        min_y = min(y for _, _, y in srm_holes)
        max_y = max(y for _, _, y in srm_holes)
        
        width = max_x - min_x
        height = max_y - min_y
        
        print(f"\nRectangle dimensions:")
        print(f"  Width: {width:.2f} mm")
        print(f"  Height: {height:.2f} mm")
        
        expected_width = 30.0  # mm
        expected_height = 30.0  # mm
        width_tolerance = 0.1  # mm
        height_tolerance = 0.1  # mm
        
        width_match = abs(width - expected_width) <= width_tolerance
        height_match = abs(height - expected_height) <= height_tolerance
        
        if width_match and height_match:
            print("\n✓ SRM mounting hole pattern matches expected dimensions (30mm x 30mm)")
        else:
            print("\n✗ SRM mounting hole pattern does not match expected dimensions")
            print(f"  Expected: {expected_width:.2f} mm x {expected_height:.2f} mm")
            print(f"  Actual: {width:.2f} mm x {height:.2f} mm")
    
    return True

if __name__ == "__main__":
    check_srm_mounting_holes()
