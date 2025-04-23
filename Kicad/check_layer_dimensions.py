import pcbnew
import os

def check_layer_dimensions():
    print("Checking layer footprint dimensions...")
    
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
    
    expected_width_mm = 264.0
    expected_height_mm = 267.0
    width_tolerance_mm = 0.5
    height_tolerance_mm = 0.5
    
    width_match = abs(width_mm - expected_width_mm) <= width_tolerance_mm
    height_match = abs(height_mm - expected_height_mm) <= height_tolerance_mm
    
    if width_match and height_match:
        print(f"✓ Board dimensions match microBTX specifications ({expected_width_mm} mm x {expected_height_mm} mm)")
    else:
        print(f"✗ Board dimensions do not match microBTX specifications")
        print(f"  Expected: {expected_width_mm} mm x {expected_height_mm} mm")
        print(f"  Actual: {width_mm:.2f} mm x {height_mm:.2f} mm")
        print(f"  Difference: {abs(width_mm - expected_width_mm):.2f} mm x {abs(height_mm - expected_height_mm):.2f} mm")
    
    layer_count = board.GetCopperLayerCount()
    print(f"\nCopper layer count: {layer_count}")
    
    print("\nChecking individual layer dimensions:")
    for layer_id in range(pcbnew.PCB_LAYER_ID_COUNT):
        if board.IsLayerEnabled(layer_id):
            layer_name = board.GetLayerName(layer_id)
            
            tracks_on_layer = [track for track in board.GetTracks() if track.IsOnLayer(layer_id)]
            
            zones_on_layer = [zone for zone in board.Zones() if zone.IsOnLayer(layer_id)]
            
            footprints_on_layer = []
            for footprint in board.GetFootprints():
                if any(pad.IsOnLayer(layer_id) for pad in footprint.Pads()):
                    footprints_on_layer.append(footprint)
            
            if tracks_on_layer or zones_on_layer or footprints_on_layer:
                print(f"  Layer {layer_id} ({layer_name}):")
                print(f"    Tracks: {len(tracks_on_layer)}")
                print(f"    Zones: {len(zones_on_layer)}")
                print(f"    Footprints with elements: {len(footprints_on_layer)}")
                
                if tracks_on_layer or zones_on_layer or footprints_on_layer:
                    min_x = float('inf')
                    min_y = float('inf')
                    max_x = float('-inf')
                    max_y = float('-inf')
                    
                    for track in tracks_on_layer:
                        start_x = track.GetStart().x / 1000000.0
                        start_y = track.GetStart().y / 1000000.0
                        end_x = track.GetEnd().x / 1000000.0
                        end_y = track.GetEnd().y / 1000000.0
                        
                        min_x = min(min_x, start_x, end_x)
                        min_y = min(min_y, start_y, end_y)
                        max_x = max(max_x, start_x, end_x)
                        max_y = max(max_y, start_y, end_y)
                    
                    for zone in zones_on_layer:
                        zone_bbox = zone.GetBoundingBox()
                        zone_min_x = zone_bbox.GetX() / 1000000.0
                        zone_min_y = zone_bbox.GetY() / 1000000.0
                        zone_max_x = (zone_bbox.GetX() + zone_bbox.GetWidth()) / 1000000.0
                        zone_max_y = (zone_bbox.GetY() + zone_bbox.GetHeight()) / 1000000.0
                        
                        min_x = min(min_x, zone_min_x)
                        min_y = min(min_y, zone_min_y)
                        max_x = max(max_x, zone_max_x)
                        max_y = max(max_y, zone_max_y)
                    
                    for footprint in footprints_on_layer:
                        fp_bbox = footprint.GetBoundingBox()
                        fp_min_x = fp_bbox.GetX() / 1000000.0
                        fp_min_y = fp_bbox.GetY() / 1000000.0
                        fp_max_x = (fp_bbox.GetX() + fp_bbox.GetWidth()) / 1000000.0
                        fp_max_y = (fp_bbox.GetY() + fp_bbox.GetHeight()) / 1000000.0
                        
                        min_x = min(min_x, fp_min_x)
                        min_y = min(min_y, fp_min_y)
                        max_x = max(max_x, fp_max_x)
                        max_y = max(max_y, fp_max_y)
                    
                    if min_x != float('inf') and min_y != float('inf') and max_x != float('-inf') and max_y != float('-inf'):
                        layer_width = max_x - min_x
                        layer_height = max_y - min_y
                        print(f"    Layer dimensions: {layer_width:.2f} mm x {layer_height:.2f} mm")
                        
                        layer_width_match = abs(layer_width - width_mm) <= width_tolerance_mm
                        layer_height_match = abs(layer_height - height_mm) <= height_tolerance_mm
                        
                        if layer_width_match and layer_height_match:
                            print(f"    ✓ Layer dimensions match board dimensions")
                        else:
                            print(f"    ✗ Layer dimensions do not match board dimensions")
                            print(f"      Difference: {abs(layer_width - width_mm):.2f} mm x {abs(layer_height - height_mm):.2f} mm")
    
    return True

if __name__ == "__main__":
    check_layer_dimensions()
