import pcbnew
import os
import subprocess
import re

def run_drc_check():
    print("Running Design Rule Check (DRC) on microBTX PCB...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    backup_file = "neotron-pico-btx.kicad_pcb.drc_backup"
    if not os.path.exists(backup_file):
        os.system(f"cp {pcb_file} {backup_file}")
        print(f"Created backup: {backup_file}")
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    board_bbox = board.GetBoardEdgesBoundingBox()
    board_width = board_bbox.GetWidth() / 1000000.0  # Convert to mm
    board_height = board_bbox.GetHeight() / 1000000.0
    print(f"Board dimensions: {board_width:.2f} mm x {board_height:.2f} mm")
    
    print("\nRunning DRC using KiCad CLI...")
    drc_output_file = "drc_output.txt"
    
    try:
        result = subprocess.run(["which", "kicad-cli"], capture_output=True, text=True)
        if result.returncode != 0:
            print("kicad-cli not found. Using pcbnew Python API for DRC instead.")
            use_cli = False
        else:
            print(f"Found kicad-cli at: {result.stdout.strip()}")
            use_cli = True
        
        if use_cli:
            cmd = ["kicad-cli", "pcb", "drc", "run", "--output-format", "json", "--output", drc_output_file, pcb_file]
            print(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"DRC failed with return code {result.returncode}")
                print(f"Error output: {result.stderr}")
                
                use_cli = False
            else:
                print("DRC completed successfully using kicad-cli")
                
                if os.path.exists(drc_output_file):
                    with open(drc_output_file, 'r') as f:
                        drc_output = f.read()
                    
                    print(f"\nDRC output file content ({drc_output_file}):")
                    print(drc_output)
                    
                    try:
                        import json
                        drc_data = json.loads(drc_output)
                        
                        violation_count = len(drc_data.get("violations", []))
                        print(f"\nFound {violation_count} DRC violations")
                        
                        if violation_count > 0:
                            print("\nDRC Violations:")
                            for i, violation in enumerate(drc_data.get("violations", [])):
                                print(f"  {i+1}. {violation.get('rule', 'Unknown rule')}: {violation.get('message', 'No message')}")
                                if i >= 9:  # Show only first 10 violations
                                    print(f"  ... and {violation_count - 10} more violations")
                                    break
                    except json.JSONDecodeError:
                        print("Failed to parse DRC output as JSON")
                        print("Raw output:")
                        print(drc_output)
                else:
                    print(f"DRC output file {drc_output_file} not found")
        
        if not use_cli:
            print("\nRunning DRC using pcbnew Python API...")
            
            drc = pcbnew.DRC(board)
            drc_prms = drc.GetDRCSettings()
            
            drc_result = drc.TestZonesOverlap()
            if drc_result:
                print("Zone overlap check failed")
            else:
                print("Zone overlap check passed")
            
            drc_result = drc.TestZonesToZonesCollisions()
            if drc_result:
                print("Zone to zone collision check failed")
            else:
                print("Zone to zone collision check passed")
            
            markers = board.GetDRCMarkers()
            marker_count = len(markers)
            
            print(f"\nFound {marker_count} DRC markers")
            
            if marker_count > 0:
                print("\nDRC Markers:")
                for i, marker in enumerate(markers):
                    print(f"  {i+1}. {marker.GetReporter().ShowReport()}")
                    if i >= 9:  # Show only first 10 markers
                        print(f"  ... and {marker_count - 10} more markers")
                        break
    
    except Exception as e:
        print(f"Error running DRC: {e}")
    
    print("\nChecking for common issues...")
    
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
        
        if (fp_min_x < board_bbox.GetX() or fp_min_y < board_bbox.GetY() or 
            fp_max_x > board_bbox.GetX() + board_bbox.GetWidth() or 
            fp_max_y > board_bbox.GetY() + board_bbox.GetHeight()):
            outside_footprints.append((ref, fp_min_x / 1000000.0, fp_min_y / 1000000.0, 
                                      fp_max_x / 1000000.0, fp_max_y / 1000000.0))
    
    if outside_footprints:
        print(f"\n✗ {len(outside_footprints)} components are outside board outline:")
        for ref, min_x, min_y, max_x, max_y in outside_footprints[:5]:  # Show first 5 for brevity
            print(f"  {ref}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})")
        if len(outside_footprints) > 5:
            print(f"  ... and {len(outside_footprints) - 5} more")
    else:
        print(f"\n✓ All {len(footprints)} components are within board outline")
    
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
        
        if (zone_min_x < board_bbox.GetX() or zone_min_y < board_bbox.GetY() or 
            zone_max_x > board_bbox.GetX() + board_bbox.GetWidth() or 
            zone_max_y > board_bbox.GetY() + board_bbox.GetHeight()):
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
    
    tracks = list(board.GetTracks())
    outside_tracks = []
    
    for track in tracks:
        start_x = track.GetStart().x
        start_y = track.GetStart().y
        end_x = track.GetEnd().x
        end_y = track.GetEnd().y
        
        if (start_x < board_bbox.GetX() or start_y < board_bbox.GetY() or 
            start_x > board_bbox.GetX() + board_bbox.GetWidth() or 
            start_y > board_bbox.GetY() + board_bbox.GetHeight() or
            end_x < board_bbox.GetX() or end_y < board_bbox.GetY() or 
            end_x > board_bbox.GetX() + board_bbox.GetWidth() or 
            end_y > board_bbox.GetY() + board_bbox.GetHeight()):
            outside_tracks.append((track.GetLayer(), 
                                  start_x / 1000000.0, start_y / 1000000.0,
                                  end_x / 1000000.0, end_y / 1000000.0))
    
    if outside_tracks:
        print(f"\n✗ {len(outside_tracks)} tracks extend beyond board outline")
        for layer, start_x, start_y, end_x, end_y in outside_tracks[:5]:  # Show first 5 for brevity
            layer_name = board.GetLayerName(layer)
            print(f"  Track on {layer_name}: ({start_x:.2f}, {start_y:.2f}) to ({end_x:.2f}, {end_y:.2f})")
        if len(outside_tracks) > 5:
            print(f"  ... and {len(outside_tracks) - 5} more")
    else:
        print(f"\n✓ No tracks extend beyond board outline (total tracks: {len(tracks)})")
    
    drc_report_file = "../documentation/btx_conversion/drc_report.md"
    
    with open(drc_report_file, 'w') as f:
        f.write("# Design Rule Check (DRC) Report\n\n")
        f.write("## Overview\n\n")
        f.write(f"This document reports the results of a Design Rule Check (DRC) on the Neotron-Pico microBTX PCB conversion.\n\n")
        
        f.write("## Board Information\n\n")
        f.write(f"- Board dimensions: {board_width:.2f} mm x {board_height:.2f} mm\n")
        f.write(f"- Total components: {len(footprints)}\n")
        f.write(f"- Total copper zones: {len(zones)}\n")
        f.write(f"- Total tracks: {len(tracks)}\n\n")
        
        f.write("## DRC Results\n\n")
        
        if use_cli:
            f.write("DRC was performed using KiCad CLI.\n\n")
            
            if os.path.exists(drc_output_file):
                try:
                    import json
                    with open(drc_output_file, 'r') as drc_file:
                        drc_output = drc_file.read()
                    
                    drc_data = json.loads(drc_output)
                    violation_count = len(drc_data.get("violations", []))
                    
                    f.write(f"Found {violation_count} DRC violations.\n\n")
                    
                    if violation_count > 0:
                        f.write("### DRC Violations\n\n")
                        for i, violation in enumerate(drc_data.get("violations", [])):
                            f.write(f"{i+1}. **{violation.get('rule', 'Unknown rule')}**: {violation.get('message', 'No message')}\n")
                            if 'locations' in violation:
                                f.write("   - Locations:\n")
                                for loc in violation.get('locations', []):
                                    f.write(f"     - ({loc.get('x', 0)/1000000.0:.2f}, {loc.get('y', 0)/1000000.0:.2f})\n")
                            f.write("\n")
                except Exception as e:
                    f.write(f"Failed to parse DRC output: {e}\n\n")
            else:
                f.write(f"DRC output file {drc_output_file} not found.\n\n")
        else:
            f.write("DRC was performed using pcbnew Python API.\n\n")
            
            marker_count = len(board.GetDRCMarkers())
            f.write(f"Found {marker_count} DRC markers.\n\n")
            
            if marker_count > 0:
                f.write("### DRC Markers\n\n")
                for i, marker in enumerate(board.GetDRCMarkers()):
                    f.write(f"{i+1}. {marker.GetReporter().ShowReport()}\n\n")
        
        f.write("## Common Issues\n\n")
        
        f.write("### Components Outside Board Outline\n\n")
        if outside_footprints:
            f.write(f"❌ {len(outside_footprints)} components are outside board outline:\n\n")
            for ref, min_x, min_y, max_x, max_y in outside_footprints:
                f.write(f"- {ref}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})\n")
            f.write("\n")
        else:
            f.write(f"✅ All {len(footprints)} components are within board outline.\n\n")
        
        f.write("### Copper Zones Outside Board Outline\n\n")
        if outside_zones:
            f.write(f"❌ {len(outside_zones)} copper zones extend beyond board outline:\n\n")
            for layer_name, min_x, min_y, max_x, max_y in outside_zones:
                f.write(f"- Zone on {layer_name}: ({min_x:.2f}, {min_y:.2f}) to ({max_x:.2f}, {max_y:.2f})\n")
            f.write("\n")
        else:
            f.write(f"✅ All {len(zones)} copper zones are within board outline.\n\n")
        
        f.write("### Tracks Outside Board Outline\n\n")
        if outside_tracks:
            f.write(f"❌ {len(outside_tracks)} tracks extend beyond board outline:\n\n")
            for layer, start_x, start_y, end_x, end_y in outside_tracks[:10]:  # Show first 10 for brevity
                layer_name = board.GetLayerName(layer)
                f.write(f"- Track on {layer_name}: ({start_x:.2f}, {start_y:.2f}) to ({end_x:.2f}, {end_y:.2f})\n")
            if len(outside_tracks) > 10:
                f.write(f"- ... and {len(outside_tracks) - 10} more\n")
            f.write("\n")
        else:
            f.write(f"✅ No tracks extend beyond board outline (total tracks: {len(tracks)}).\n\n")
        
        f.write("## Conclusion\n\n")
        
        if outside_footprints or outside_zones or outside_tracks or (use_cli and os.path.exists(drc_output_file) and len(json.loads(drc_output)) > 0) or (not use_cli and len(board.GetDRCMarkers()) > 0):
            f.write("❌ The PCB has DRC violations that need to be addressed.\n\n")
            
            f.write("### Recommended Actions\n\n")
            
            if outside_footprints:
                f.write("1. Reposition components that extend beyond the board outline.\n")
            
            if outside_zones:
                f.write("2. Adjust copper zones to match the board outline.\n")
            
            if outside_tracks:
                f.write("3. Reroute tracks that extend beyond the board outline.\n")
            
            if (use_cli and os.path.exists(drc_output_file) and len(json.loads(drc_output)) > 0) or (not use_cli and len(board.GetDRCMarkers()) > 0):
                f.write("4. Address other DRC violations reported by KiCad.\n")
        else:
            f.write("✅ The PCB passes all DRC checks.\n")
    
    print(f"\nDRC report saved to {drc_report_file}")
    
    return True

if __name__ == "__main__":
    run_drc_check()
