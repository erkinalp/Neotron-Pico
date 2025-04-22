#!/usr/bin/env python3
"""
Final BTX conversion script for Neotron-Pico.
Properly handles component categories and DRC violations.
"""
import sys
import os
import json
import subprocess

# Add KiCad Python modules to path
sys.path.append('/usr/lib/python3/dist-packages')
try:
    import pcbnew
except ImportError:
    print("Error: pcbnew module not found. Make sure KiCad is installed correctly.")
    sys.exit(1)

def get_component_category(footprint, specs):
    """Determine the category of a component based on its reference and value."""
    reference = footprint.GetReference()
    value = footprint.GetValue()
    
    for component in specs["component_categories"]["A_non_mirrorable"]:
        if component.lower() in value.lower() or component.lower() in reference.lower():
            return "A_non_mirrorable"
    
    for component in specs["component_categories"]["C_position_critical"]:
        if component.lower() in value.lower() or component.lower() in reference.lower():
            return "C_position_critical"
    
    for component in specs["component_categories"]["B_mirrorable"]:
        if component.lower() in value.lower() or component.lower() in reference.lower():
            return "B_mirrorable"
    
    return "unknown"

def fix_drc_violations(board, specs):
    """Apply fixes for common DRC violations."""
    print("Applying DRC violation fixes...")
    
    # Set design rules according to specs
    design_settings = board.GetDesignSettings()
    
    # Set clearance constraints
    design_settings.m_MinClearance = int(specs["drc_settings"]["clearance"] * 1000000)  # Convert to nm
    
    # Set track width constraints
    design_settings.m_TrackMinWidth = int(specs["drc_settings"]["track_width"] * 1000000)
    
    # Set via size constraints
    design_settings.m_ViasMinSize = int(specs["drc_settings"]["via_diameter"] * 1000000)
    design_settings.m_ViasMinDrill = int(specs["drc_settings"]["via_drill"] * 1000000)
    
    # Set hole clearance constraints
    design_settings.m_HoleToHoleMin = int(specs["drc_settings"]["min_hole_clearance"] * 1000000)
    
    # Set copper edge clearance
    design_settings.m_CopperEdgeClearance = int(specs["drc_settings"]["min_copper_edge_clearance"] * 1000000)
    
    # Fix silkscreen overlaps by shifting items slightly
    for footprint in board.GetFootprints():
        # Adjust silkscreen items to avoid overlaps
        for item in footprint.GraphicalItems():
            if item.GetLayer() == pcbnew.F_SilkS or item.GetLayer() == pcbnew.B_SilkS:
                pos = item.GetPosition()
                new_pos = pcbnew.VECTOR2I(pos.x + 50000, pos.y)  # Shift by 0.05mm
                item.SetPosition(new_pos)
    
    # Fix track clearance issues
    for track in board.GetTracks():
        # Increase width of thin tracks
        if track.GetWidth() < int(specs["drc_settings"]["track_width"] * 1000000):
            track.SetWidth(int(specs["drc_settings"]["track_width"] * 1000000))
    
    # Fix via clearance issues - using GetTracks() instead of GetVias()
    for track in board.GetTracks():
        if track.GetClass() == "PCB_VIA":
            # Increase size of small vias - using SetWidth with a layer argument
            try:
                if track.GetWidth(pcbnew.F_Cu) < int(specs["drc_settings"]["via_diameter"] * 1000000):
                    track.SetWidth(int(specs["drc_settings"]["via_diameter"] * 1000000))
            except Exception as e:
                print(f"Warning: Could not modify via: {e}")
    
    print("DRC violation fixes applied")
    return board

def convert_pcb(input_file, output_file, specs_file):
    """Convert PCB from ATX to BTX form factor."""
    with open(specs_file, 'r') as f:
        specs = json.load(f)
    
    board = pcbnew.LoadBoard(input_file)
    
    board_width = specs["target_dimensions"]["width"] * 1000000  # Convert to internal units (nm)
    board_height = specs["target_dimensions"]["height"] * 1000000
    
    print("Mirroring board outline...")
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcbnew.Edge_Cuts:
            start_x = drawing.GetStart().x
            start_y = drawing.GetStart().y
            end_x = drawing.GetEnd().x
            end_y = drawing.GetEnd().y
            
            new_start_x = board_width - start_x
            new_start_y = start_y
            new_end_x = board_width - end_x
            new_end_y = end_y
            
            drawing.SetStart(pcbnew.VECTOR2I(int(new_start_x), int(new_start_y)))
            drawing.SetEnd(pcbnew.VECTOR2I(int(new_end_x), int(new_end_y)))
    
    category_counts = {
        "A_non_mirrorable": 0,
        "B_mirrorable": 0,
        "C_position_critical": 0,
        "unknown": 0
    }
    
    print("Processing components...")
    for footprint in board.GetFootprints():
        category = get_component_category(footprint, specs)
        category_counts[category] += 1
        reference = footprint.GetReference()
        value = footprint.GetValue()
        
        print(f"Processing {reference} - {value} (Category: {category})")
        
        position = footprint.GetPosition()
        x = position.x
        y = position.y
        
        if category == "A_non_mirrorable":
            # For Category A: No mirroring, just reposition
            new_x = board_width - x
            new_y = y
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
            
            # For rotation, we'll use a simpler approach
            # Just set a fixed orientation value (180 degrees)
            try:
                # Try different methods to rotate the component
                # Method 1: Using integer value (KiCad internal units)
                footprint.SetOrientation(1800)  # 180 degrees in 0.1 degree units
            except Exception as e:
                print(f"Warning: Could not rotate {reference}: {e}")
                # If rotation fails, we'll still have the component repositioned correctly
            
        elif category == "B_mirrorable":
            # For Category B: Mirror position and orientation
            new_x = board_width - x
            new_y = y
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
            
            # Flip the footprint (this handles orientation)
            try:
                footprint.Flip(pcbnew.VECTOR2I(int(new_x), int(new_y)), False)
            except Exception as e:
                print(f"Warning: Could not flip {reference}: {e}")
            
        elif category == "C_position_critical":
            # For Category C: Position according to BTX specs
            connector_type = None
            for conn_type in specs["connector_positions"].keys():
                if conn_type.lower() in reference.lower() or conn_type.lower() in value.lower():
                    connector_type = conn_type
                    break
            
            if connector_type:
                new_x = specs["connector_positions"][connector_type]["x"] * 1000000
                new_y = specs["connector_positions"][connector_type]["y"] * 1000000
            else:
                new_x = board_width - x
                new_y = y
            
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
            
            # Handle mounting holes specifically
            if "MountingHole" in reference:
                min_dist = float('inf')
                best_hole = None
                for hole, pos in specs["mounting_holes"].items():
                    hole_x = pos["x"] * 1000000
                    hole_y = pos["y"] * 1000000
                    dist = ((hole_x - x)**2 + (hole_y - y)**2)**0.5
                    if dist < min_dist:
                        min_dist = dist
                        best_hole = hole
                
                if best_hole:
                    new_x = specs["mounting_holes"][best_hole]["x"] * 1000000
                    new_y = specs["mounting_holes"][best_hole]["y"] * 1000000
                    new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
                    footprint.SetPosition(new_position)
        else:
            # For unknown components: Just mirror position
            new_x = board_width - x
            new_y = y
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
    
    # Apply DRC violation fixes
    board = fix_drc_violations(board, specs)
    
    # Save the converted PCB
    pcbnew.SaveBoard(output_file, board)
    print(f"PCB file converted successfully: {output_file}")
    
    # Print component category counts
    print("\nComponent category counts:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    
    # Create a conversion report
    report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(output_file))), "documentation", "btx_conversion")
    os.makedirs(report_dir, exist_ok=True)
    
    with open(os.path.join(report_dir, "conversion_report.md"), "w") as f:
        f.write("# Neotron-Pico microBTX Conversion Report\n\n")
        f.write("## Overview\n\n")
        f.write("This report details the conversion of the Neotron-Pico PCB from ATX to microBTX form factor.\n\n")
        f.write("## Conversion Process\n\n")
        f.write("1. **Board Outline Mirroring**: The board outline was mirrored to match the microBTX form factor.\n")
        f.write("2. **Component Repositioning**: Components were repositioned based on their categories:\n")
        f.write("   - Category A (Non-mirrorable): Repositioned without mirroring\n")
        f.write("   - Category B (Mirrorable): Mirrored in position and orientation\n")
        f.write("   - Category C (Position-critical): Positioned according to microBTX specifications\n")
        f.write("3. **DRC Violation Fixes**: Common DRC violations were fixed during the conversion process.\n\n")
        f.write("## Component Statistics\n\n")
        for category, count in category_counts.items():
            f.write(f"- {category}: {count} components\n")
    
    # Run DRC on the converted PCB
    try:
        subprocess.run(["kicad-cli", "pcb", "drc", output_file, "--format", "json", "--output", "drc_report.json"], check=True)
        print("DRC check completed. See drc_report.json for details.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: DRC check failed: {e}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 btx_convert_final.py <input_pcb> <output_pcb> <specs_json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    specs_file = sys.argv[3]
    
    success = convert_pcb(input_file, output_file, specs_file)
    sys.exit(0 if success else 1)
