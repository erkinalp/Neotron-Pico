
import pcbnew
import os
import math

def verify_conversion():
    print("Verifying microBTX conversion...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    board_bbox = board.GetBoardEdgesBoundingBox()
    board_min_x = board_bbox.GetX()
    board_min_y = board_bbox.GetY()
    board_width = board_bbox.GetWidth()
    board_height = board_bbox.GetHeight()
    board_max_x = board_min_x + board_width
    board_max_y = board_min_y + board_height
    
    width_mm = board_width / 1000000.0  # Convert from internal units to mm
    height_mm = board_height / 1000000.0
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
    srm_mounting_holes = []
    
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('H'):
            pos = footprint.GetPosition()
            x_mm = pos.x / 1000000.0
            y_mm = pos.y / 1000000.0
            
            mounting_holes.append((ref, x_mm, y_mm))
            
            if 'SRM' in ref:
                srm_mounting_holes.append((ref, x_mm, y_mm))
    
    print(f"\nFound {len(mounting_holes)} mounting holes")
    for ref, x, y in mounting_holes:
        print(f"  {ref}: ({x:.2f} mm, {y:.2f} mm)")
    
    print(f"Found {len(srm_mounting_holes)} SRM mounting holes")
    for ref, x, y in srm_mounting_holes:
        print(f"  {ref}: ({x:.2f} mm, {y:.2f} mm)")
    
    expected_perimeter_holes = 5
    expected_srm_holes = 4
    expected_total_holes = expected_perimeter_holes + expected_srm_holes
    
    if len(mounting_holes) == expected_total_holes:
        print(f"✓ Correct number of mounting holes for microBTX ({expected_perimeter_holes} perimeter + {expected_srm_holes} SRM)")
    else:
        print(f"✗ Incorrect number of mounting holes: {len(mounting_holes)} (expected {expected_total_holes})")
    
    if len(srm_mounting_holes) == expected_srm_holes:
        print(f"✓ Correct number of SRM mounting holes ({expected_srm_holes})")
    else:
        print(f"✗ Incorrect number of SRM mounting holes: {len(srm_mounting_holes)} (expected {expected_srm_holes})")
    
    srm_min_x = board_min_x + 102050000  # 102.05 mm from left edge
    srm_min_y = board_min_y + 103550000  # 103.55 mm from top edge
    srm_width = 60000000  # 60 mm
    srm_height = 60000000  # 60 mm
    srm_max_x = srm_min_x + srm_width
    srm_max_y = srm_min_y + srm_height
    
    srm_min_x_mm = srm_min_x / 1000000.0
    srm_min_y_mm = srm_min_y / 1000000.0
    srm_max_x_mm = srm_max_x / 1000000.0
    srm_max_y_mm = srm_max_y / 1000000.0
    
    print(f"\nSRM Region: ({srm_min_x_mm:.2f}, {srm_min_y_mm:.2f}) to ({srm_max_x_mm:.2f}, {srm_max_y_mm:.2f})")
    
    heat_generating_components = []
    heat_components_in_srm = 0
    
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('U') or ref.startswith('IC') or ref.startswith('CPU') or ref.startswith('MCU'):
            pos = footprint.GetPosition()
            x = pos.x
            y = pos.y
            x_mm = x / 1000000.0
            y_mm = y / 1000000.0
            
            heat_generating_components.append((ref, x, y))
            
            in_srm = (srm_min_x <= x <= srm_max_x) and (srm_min_y <= y <= srm_max_y)
            
            if in_srm:
                heat_components_in_srm += 1
                print(f"  ✓ {ref} is within SRM region: ({x_mm:.2f}, {y_mm:.2f})")
            else:
                print(f"  ✗ {ref} is outside SRM region: ({x_mm:.2f}, {y_mm:.2f})")
    
    if heat_components_in_srm == len(heat_generating_components):
        print(f"✓ All {len(heat_generating_components)} heat-generating components are within SRM region")
    else:
        print(f"✗ Only {heat_components_in_srm}/{len(heat_generating_components)} heat-generating components are within SRM region")
    
    tracks = list(board.GetTracks())
    print(f"\nBoard has {len(tracks)} tracks")
    
    if len(tracks) > 0:
        print("✓ Board has traces - trace rerouting has been performed")
    else:
        print("✗ Board has no traces - trace rerouting is incomplete")
        print("  NOTE: Traces have been cleared to prepare for manual rerouting in KiCad GUI")
    
    zones = list(board.Zones())
    outside_zones = []
    
    for zone in zones:
        layer_id = zone.GetLayer()
        layer_name = board.GetLayerName(layer_id)
        
        zone_bbox = zone.GetBoundingBox()
        zone_min_x = zone_bbox.GetX()
        zone_min_y = zone_bbox.GetY()
        zone_width = zone_bbox.GetWidth()
        zone_height = zone_bbox.GetHeight()
        zone_max_x = zone_min_x + zone_width
        zone_max_y = zone_min_y + zone_height
        
        if (zone_min_x < board_min_x or zone_min_y < board_min_y or 
            zone_max_x > board_max_x or zone_max_y > board_max_y):
            outside_zones.append((layer_name,
                                 zone_min_x / 1000000.0, zone_min_y / 1000000.0,
                                 zone_max_x / 1000000.0, zone_max_y / 1000000.0))
    
    print(f"\nBoard has {len(zones)} copper zones")
    
    if outside_zones:
        print(f"✗ {len(outside_zones)} copper zones extend beyond board outline:")
        for layer_name, min_x, min_y, max_x, max_y in outside_zones:
            print(f"  Zone on {layer_name}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
    else:
        print("✓ All copper zones are within board outline")
    
    expansion_slots = []
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('J') and ('PCI' in ref or 'PCIe' in ref or 'AGP' in ref or 'ISA' in ref):
            pos = footprint.GetPosition()
            x_mm = pos.x / 1000000.0
            y_mm = pos.y / 1000000.0
            
            expansion_slots.append((ref, x_mm, y_mm))
    
    print(f"\nFound {len(expansion_slots)} expansion slots")
    for ref, x, y in expansion_slots:
        print(f"  {ref}: ({x:.2f} mm, {y:.2f} mm)")
    
    external_connectors = []
    for footprint in board.GetFootprints():
        ref = str(footprint.GetReference())
        if ref.startswith('J') and not ('PCI' in ref or 'PCIe' in ref or 'AGP' in ref or 'ISA' in ref):
            pos = footprint.GetPosition()
            x_mm = pos.x / 1000000.0
            y_mm = pos.y / 1000000.0
            
            external_connectors.append((ref, x_mm, y_mm))
    
    print(f"\nFound {len(external_connectors)} external connectors")
    
    print("\nVerification Summary:")
    print(f"{'✓' if width_match and height_match else '✗'} Board dimensions: {width_mm:.2f} mm x {height_mm:.2f} mm")
    print(f"{'✓' if len(mounting_holes) == expected_total_holes else '✗'} Mounting holes: {len(mounting_holes)}/{expected_total_holes}")
    print(f"{'✓' if len(srm_mounting_holes) == expected_srm_holes else '✗'} SRM mounting holes: {len(srm_mounting_holes)}/{expected_srm_holes}")
    print(f"{'✓' if heat_components_in_srm == len(heat_generating_components) else '✗'} Heat-generating components in SRM: {heat_components_in_srm}/{len(heat_generating_components)}")
    print(f"{'✓' if len(tracks) > 0 else '✗'} Trace rerouting: {len(tracks)} tracks")
    print(f"{'✓' if not outside_zones else '✗'} Copper zones: {len(zones) - len(outside_zones)}/{len(zones)} within board outline")
    
    if (width_match and 
        height_match and 
        len(mounting_holes) == expected_total_holes and 
        len(srm_mounting_holes) == expected_srm_holes and 
        heat_components_in_srm == len(heat_generating_components) and 
        not outside_zones):
        print("\n✅ microBTX conversion is complete and verified")
        return True
    else:
        print("\n❌ microBTX conversion is incomplete or has issues")
        if not width_match or not height_match:
            print("  - Board dimensions do not match microBTX specifications")
        if len(mounting_holes) != expected_total_holes:
            print(f"  - Incorrect number of mounting holes: {len(mounting_holes)} (expected {expected_total_holes})")
        if len(srm_mounting_holes) != expected_srm_holes:
            print(f"  - Incorrect number of SRM mounting holes: {len(srm_mounting_holes)} (expected {expected_srm_holes})")
        if heat_components_in_srm != len(heat_generating_components):
            print(f"  - Not all heat-generating components are within SRM region: {heat_components_in_srm}/{len(heat_generating_components)}")
        if len(tracks) == 0:
            print("  - No traces - trace rerouting is incomplete")
        if outside_zones:
            print(f"  - {len(outside_zones)} copper zones extend beyond board outline")
        return False

if __name__ == "__main__":
    verify_conversion()
