import pcbnew
import os

def detailed_layer_analysis():
    print("Detailed layer dimension analysis...")
    
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
    
    print("\nFootprint positions:")
    footprints = list(board.GetFootprints())
    print(f"Total footprints: {len(footprints)}")
    
    outside_footprints = []
    for fp in footprints:
        fp_bbox = fp.GetBoundingBox()
        fp_min_x = fp_bbox.GetX()
        fp_min_y = fp_bbox.GetY()
        fp_width = fp_bbox.GetWidth()
        fp_height = fp_bbox.GetHeight()
        fp_max_x = fp_min_x + fp_width
        fp_max_y = fp_min_y + fp_height
        
        if (fp_min_x < board_min_x or fp_min_y < board_min_y or 
            fp_max_x > board_max_x or fp_max_y > board_max_y):
            outside_footprints.append((fp.GetReference(), 
                                      fp_min_x / 1000000.0, fp_min_y / 1000000.0,
                                      fp_max_x / 1000000.0, fp_max_y / 1000000.0))
    
    if outside_footprints:
        print("\nFootprints outside board outline:")
        for ref, min_x, min_y, max_x, max_y in outside_footprints:
            print(f"  {ref}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
        print(f"Total footprints outside board outline: {len(outside_footprints)}")
    else:
        print("\nNo footprints outside board outline")
    
    print("\nTrack positions:")
    tracks = list(board.GetTracks())
    print(f"Total tracks: {len(tracks)}")
    
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
        print("\nTracks outside board outline:")
        print(f"Total tracks outside board outline: {len(outside_tracks)}")
        print(f"Sample of 5 tracks outside board outline:")
        for i, (layer, start_x, start_y, end_x, end_y) in enumerate(outside_tracks[:5]):
            layer_name = board.GetLayerName(layer)
            print(f"  Track on {layer_name}: ({start_x:.2f}, {start_y:.2f}) to ({end_x:.2f}, {end_y:.2f})")
    else:
        print("\nNo tracks outside board outline")
    
    print("\nZone positions:")
    zones = list(board.Zones())
    print(f"Total zones: {len(zones)}")
    
    outside_zones = []
    for zone in zones:
        zone_bbox = zone.GetBoundingBox()
        zone_min_x = zone_bbox.GetX()
        zone_min_y = zone_bbox.GetY()
        zone_width = zone_bbox.GetWidth()
        zone_height = zone_bbox.GetHeight()
        zone_max_x = zone_min_x + zone_width
        zone_max_y = zone_min_y + zone_height
        
        if (zone_min_x < board_min_x or zone_min_y < board_min_y or 
            zone_max_x > board_max_x or zone_max_y > board_max_y):
            layer_id = zone.GetLayer()
            layer_name = board.GetLayerName(layer_id)
            outside_zones.append((layer_name,
                                 zone_min_x / 1000000.0, zone_min_y / 1000000.0,
                                 zone_max_x / 1000000.0, zone_max_y / 1000000.0))
    
    if outside_zones:
        print("\nZones outside board outline:")
        for layer_name, min_x, min_y, max_x, max_y in outside_zones:
            print(f"  Zone on {layer_name}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
        print(f"Total zones outside board outline: {len(outside_zones)}")
    else:
        print("\nNo zones outside board outline")
    
    return True

if __name__ == "__main__":
    detailed_layer_analysis()
