import pcbnew
import os

def verify_modifications():
    print("Verifying PCB modifications for microBTX compliance...")
    
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
    
    print(f"Board dimensions: {board_width / 1000000.0:.2f} mm x {board_height / 1000000.0:.2f} mm")
    print(f"Board bounds: ({board_min_x / 1000000.0:.2f}, {board_min_y / 1000000.0:.2f}) to ({board_max_x / 1000000.0:.2f}, {board_max_y / 1000000.0:.2f})")
    
    expected_width_mm = 264.0
    expected_height_mm = 267.0
    tolerance_mm = 0.5
    
    width_match = abs(board_width / 1000000.0 - expected_width_mm) <= tolerance_mm
    height_match = abs(board_height / 1000000.0 - expected_height_mm) <= tolerance_mm
    
    if width_match and height_match:
        print(f"✓ Board dimensions match microBTX specifications ({expected_width_mm} mm x {expected_height_mm} mm)")
    else:
        print(f"✗ Board dimensions do not match microBTX specifications")
        print(f"  Expected: {expected_width_mm} mm x {expected_height_mm} mm")
        print(f"  Actual: {board_width / 1000000.0:.2f} mm x {board_height / 1000000.0:.2f} mm")
    
    srm_min_x = board_min_x + 102050000  # 102.05 mm from left edge
    srm_min_y = board_min_y + 103550000  # 103.55 mm from top edge
    srm_width = 60000000  # 60 mm
    srm_height = 60000000  # 60 mm
    srm_max_x = srm_min_x + srm_width
    srm_max_y = srm_min_y + srm_height
    
    print(f"\nSRM region: ({srm_min_x / 1000000.0:.2f}, {srm_min_y / 1000000.0:.2f}) to ({srm_max_x / 1000000.0:.2f}, {srm_max_y / 1000000.0:.2f})")
    
    footprints = list(board.GetFootprints())
    outside_footprints = []
    
    for fp in footprints:
        ref = fp.GetReference()
        fp_bbox = fp.GetBoundingBox()
        fp_min_x = fp_bbox.GetX()
        fp_min_y = fp_bbox.GetY()
        fp_width = fp_bbox.GetWidth()
        fp_height = fp_bbox.GetHeight()
        fp_max_x = fp_min_x + fp_width
        fp_max_y = fp_min_y + fp_height
        
        if (fp_min_x < board_min_x or fp_min_y < board_min_y or 
            fp_max_x > board_max_x or fp_max_y > board_max_y):
            outside_footprints.append((ref, fp_min_x / 1000000.0, fp_min_y / 1000000.0, 
                                      fp_max_x / 1000000.0, fp_max_y / 1000000.0))
    
    if outside_footprints:
        print(f"\n✗ {len(outside_footprints)} components are still outside board outline:")
        for ref, min_x, min_y, max_x, max_y in outside_footprints[:5]:  # Show first 5 for brevity
            print(f"  {ref}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
        if len(outside_footprints) > 5:
            print(f"  ... and {len(outside_footprints) - 5} more")
    else:
        print(f"\n✓ All {len(footprints)} components are within board outline")
    
    heat_generating_refs = [ref for ref in [fp.GetReference() for fp in footprints] 
                           if ref.startswith('U') or ref.startswith('IC') or ref.startswith('CPU')]
    
    heat_components_outside_srm = []
    for ref in heat_generating_refs:
        fp = board.FindFootprintByReference(ref)
        if fp:
            fp_bbox = fp.GetBoundingBox()
            fp_center_x = fp_bbox.GetX() + fp_bbox.GetWidth() / 2
            fp_center_y = fp_bbox.GetY() + fp_bbox.GetHeight() / 2
            
            if (fp_center_x < srm_min_x or fp_center_x > srm_max_x or 
                fp_center_y < srm_min_y or fp_center_y > srm_max_y):
                heat_components_outside_srm.append((ref, fp_center_x / 1000000.0, fp_center_y / 1000000.0))
    
    if heat_components_outside_srm:
        print(f"\n✗ {len(heat_components_outside_srm)} heat-generating components are outside SRM region:")
        for ref, x, y in heat_components_outside_srm[:5]:  # Show first 5 for brevity
            print(f"  {ref}: ({x:.2f}, {y:.2f})")
        if len(heat_components_outside_srm) > 5:
            print(f"  ... and {len(heat_components_outside_srm) - 5} more")
    else:
        print(f"\n✓ All {len(heat_generating_refs)} heat-generating components are within SRM region")
    
    tracks = list(board.GetTracks())
    outside_tracks = []
    
    for track in tracks:
        start_x = track.GetStart().x
        start_y = track.GetStart().y
        end_x = track.GetEnd().x
        end_y = track.GetEnd().y
        
        if (start_x < board_min_x or start_y < board_min_y or 
            start_x > board_max_x or start_y > board_max_y or
            end_x < board_min_x or end_y < board_min_y or 
            end_x > board_max_x or end_y > board_max_y):
            outside_tracks.append((track.GetLayer(), 
                                  start_x / 1000000.0, start_y / 1000000.0,
                                  end_x / 1000000.0, end_y / 1000000.0))
    
    if outside_tracks:
        print(f"\n✗ {len(outside_tracks)} tracks extend beyond board outline")
    else:
        print(f"\n✓ No tracks extend beyond board outline (total tracks: {len(tracks)})")
    
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
    
    if outside_zones:
        print(f"\n✗ {len(outside_zones)} copper zones extend beyond board outline:")
        for layer_name, min_x, min_y, max_x, max_y in outside_zones[:5]:  # Show first 5 for brevity
            print(f"  Zone on {layer_name}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
        if len(outside_zones) > 5:
            print(f"  ... and {len(outside_zones) - 5} more")
    else:
        print(f"\n✓ All {len(zones)} copper zones are within board outline")
    
    print("\nVerification Summary:")
    print(f"✓ Board dimensions: {width_match and height_match}")
    print(f"{'✓' if not outside_footprints else '✗'} Component placement")
    print(f"{'✓' if not heat_components_outside_srm else '✗'} Heat-generating components in SRM")
    print(f"{'✓' if not outside_tracks else '✗'} Track routing")
    print(f"{'✓' if not outside_zones else '✗'} Copper zones")
    
    return True

if __name__ == "__main__":
    verify_modifications()
