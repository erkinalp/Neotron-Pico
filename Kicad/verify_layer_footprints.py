import pcbnew
import os

def verify_layer_footprints():
    print("Verifying layer footprints for microBTX compliance...")
    
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
    
    layer_count = board.GetCopperLayerCount()
    print(f"Copper layer count: {layer_count}")
    
    for layer_id in range(pcbnew.PCB_LAYER_ID_COUNT):
        if board.IsLayerEnabled(layer_id):
            layer_name = board.GetLayerName(layer_id)
            print(f"Layer {layer_id}: {layer_name}")
    
    footprints = list(board.GetFootprints())
    print(f"\nTotal footprints: {len(footprints)}")
    
    layer_footprints = {}
    for layer_id in range(pcbnew.PCB_LAYER_ID_COUNT):
        if board.IsLayerEnabled(layer_id):
            layer_name = board.GetLayerName(layer_id)
            layer_footprints[layer_name] = []
    
    for fp in footprints:
        ref = fp.GetReference()
        layer_id = fp.GetLayer()
        layer_name = board.GetLayerName(layer_id)
        
        fp_bbox = fp.GetBoundingBox()
        fp_min_x = fp_bbox.GetX()
        fp_min_y = fp_bbox.GetY()
        fp_width = fp_bbox.GetWidth()
        fp_height = fp_bbox.GetHeight()
        fp_max_x = fp_min_x + fp_width
        fp_max_y = fp_min_y + fp_height
        
        fp_min_x_mm = fp_min_x / 1000000.0
        fp_min_y_mm = fp_min_y / 1000000.0
        fp_max_x_mm = fp_max_x / 1000000.0
        fp_max_y_mm = fp_max_y / 1000000.0
        
        layer_footprints[layer_name].append((ref, fp_min_x_mm, fp_min_y_mm, fp_max_x_mm, fp_max_y_mm))
    
    print("\nFootprint counts by layer:")
    for layer_name, fps in layer_footprints.items():
        print(f"  {layer_name}: {len(fps)} footprints")
    
    outside_footprints = []
    for fp in footprints:
        ref = fp.GetReference()
        layer_id = fp.GetLayer()
        layer_name = board.GetLayerName(layer_id)
        
        fp_bbox = fp.GetBoundingBox()
        fp_min_x = fp_bbox.GetX()
        fp_min_y = fp_bbox.GetY()
        fp_width = fp_bbox.GetWidth()
        fp_height = fp_bbox.GetHeight()
        fp_max_x = fp_min_x + fp_width
        fp_max_y = fp_min_y + fp_height
        
        if (fp_min_x < board_min_x or fp_min_y < board_min_y or 
            fp_max_x > board_max_x or fp_max_y > board_max_y):
            
            fp_min_x_mm = fp_min_x / 1000000.0
            fp_min_y_mm = fp_min_y / 1000000.0
            fp_max_x_mm = fp_max_x / 1000000.0
            fp_max_y_mm = fp_max_y / 1000000.0
            
            outside_footprints.append((ref, layer_name, fp_min_x_mm, fp_min_y_mm, fp_max_x_mm, fp_max_y_mm))
    
    if outside_footprints:
        print(f"\n✗ {len(outside_footprints)} footprints extend beyond board outline:")
        for ref, layer, min_x, min_y, max_x, max_y in outside_footprints:
            print(f"  {ref} on {layer}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
    else:
        print(f"\n✓ All {len(footprints)} footprints are within board outline")
    
    zones = list(board.Zones())
    print(f"\nTotal copper zones: {len(zones)}")
    
    layer_zones = {}
    for layer_id in range(pcbnew.PCB_LAYER_ID_COUNT):
        if board.IsLayerEnabled(layer_id):
            layer_name = board.GetLayerName(layer_id)
            layer_zones[layer_name] = []
    
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
        
        zone_min_x_mm = zone_min_x / 1000000.0
        zone_min_y_mm = zone_min_y / 1000000.0
        zone_max_x_mm = zone_max_x / 1000000.0
        zone_max_y_mm = zone_max_y / 1000000.0
        
        layer_zones[layer_name].append((zone_min_x_mm, zone_min_y_mm, zone_max_x_mm, zone_max_y_mm))
    
    print("\nZone counts by layer:")
    for layer_name, zones_list in layer_zones.items():
        if zones_list:
            print(f"  {layer_name}: {len(zones_list)} zones")
    
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
            
            zone_min_x_mm = zone_min_x / 1000000.0
            zone_min_y_mm = zone_min_y / 1000000.0
            zone_max_x_mm = zone_max_x / 1000000.0
            zone_max_y_mm = zone_max_y / 1000000.0
            
            outside_zones.append((layer_name, zone_min_x_mm, zone_min_y_mm, zone_max_x_mm, zone_max_y_mm))
    
    if outside_zones:
        print(f"\n✗ {len(outside_zones)} zones extend beyond board outline:")
        for layer, min_x, min_y, max_x, max_y in outside_zones:
            print(f"  Zone on {layer}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
    else:
        print(f"\n✓ All {len(zones)} zones are within board outline")
    
    report_file = "../documentation/btx_conversion/layer_footprint_report.md"
    
    with open(report_file, 'w') as f:
        f.write("# Layer Footprint Verification Report\n\n")
        f.write("## Overview\n\n")
        f.write(f"This document reports the results of layer footprint verification for the Neotron-Pico microBTX PCB conversion.\n\n")
        
        f.write("## Board Information\n\n")
        f.write(f"- Board dimensions: {width_mm:.2f} mm x {height_mm:.2f} mm\n")
        f.write(f"- Copper layer count: {layer_count}\n")
        f.write(f"- Total footprints: {len(footprints)}\n")
        f.write(f"- Total copper zones: {len(zones)}\n\n")
        
        f.write("## Layer Information\n\n")
        f.write("| Layer ID | Layer Name | Footprint Count | Zone Count |\n")
        f.write("|----------|------------|-----------------|------------|\n")
        
        for layer_id in range(pcbnew.PCB_LAYER_ID_COUNT):
            if board.IsLayerEnabled(layer_id):
                layer_name = board.GetLayerName(layer_id)
                footprint_count = len(layer_footprints.get(layer_name, []))
                zone_count = len(layer_zones.get(layer_name, []))
                
                f.write(f"| {layer_id} | {layer_name} | {footprint_count} | {zone_count} |\n")
        
        f.write("\n## Footprint Verification\n\n")
        
        if outside_footprints:
            f.write(f"❌ {len(outside_footprints)} footprints extend beyond board outline:\n\n")
            f.write("| Reference | Layer | Min X (mm) | Min Y (mm) | Max X (mm) | Max Y (mm) |\n")
            f.write("|-----------|-------|------------|------------|------------|------------|\n")
            
            for ref, layer, min_x, min_y, max_x, max_y in outside_footprints:
                f.write(f"| {ref} | {layer} | {min_x:.2f} | {min_y:.2f} | {max_x:.2f} | {max_y:.2f} |\n")
            
            f.write("\n")
        else:
            f.write(f"✅ All {len(footprints)} footprints are within board outline.\n\n")
        
        f.write("## Zone Verification\n\n")
        
        if outside_zones:
            f.write(f"❌ {len(outside_zones)} zones extend beyond board outline:\n\n")
            f.write("| Layer | Min X (mm) | Min Y (mm) | Max X (mm) | Max Y (mm) |\n")
            f.write("|-------|------------|------------|------------|------------|\n")
            
            for layer, min_x, min_y, max_x, max_y in outside_zones:
                f.write(f"| {layer} | {min_x:.2f} | {min_y:.2f} | {max_x:.2f} | {max_y:.2f} |\n")
            
            f.write("\n")
        else:
            f.write(f"✅ All {len(zones)} zones are within board outline.\n\n")
        
        f.write("## Conclusion\n\n")
        
        if outside_footprints or outside_zones:
            f.write("❌ The PCB has layer footprint issues that need to be addressed.\n\n")
            
            f.write("### Recommended Actions\n\n")
            
            if outside_footprints:
                f.write("1. Reposition footprints that extend beyond the board outline.\n")
            
            if outside_zones:
                f.write("2. Adjust copper zones to match the board outline.\n")
        else:
            f.write("✅ All layer footprints are within board outline and comply with microBTX specifications.\n")
    
    print(f"\nLayer footprint verification report saved to {report_file}")
    
    return True

if __name__ == "__main__":
    verify_layer_footprints()
