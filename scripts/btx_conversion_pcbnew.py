#!/usr/bin/env python3
"""
Script to convert the Neotron-Pico PCB from ATX to BTX form factor using KiCad's pcbnew API.
"""
import sys
import os
import json
import pcbnew

def mirror_board_outline(board):
    """Mirror the board outline horizontally."""
    # Get the board outline
    board_outline = board.GetBoardEdgesBoundingBox()
    print(f"Original board dimensions: {board_outline.GetWidth() / pcbnew.IU_PER_MM:.2f} x {board_outline.GetHeight() / pcbnew.IU_PER_MM:.2f} mm")
    
    # Mirror the board outline
    # This requires iterating through all drawing segments and mirroring them
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcbnew.Edge_Cuts:
            # Mirror the drawing around the Y axis
            drawing.Flip(pcbnew.VECTOR2I(0, 0), True)
    
    # Verify the new dimensions
    new_outline = board.GetBoardEdgesBoundingBox()
    print(f"New board dimensions: {new_outline.GetWidth() / pcbnew.IU_PER_MM:.2f} x {new_outline.GetHeight() / pcbnew.IU_PER_MM:.2f} mm")
    
    return board

def reposition_components(board, component_categories):
    """Reposition components according to their categories."""
    # Get all footprints
    footprints = board.GetFootprints()
    
    # Process each footprint
    for footprint in footprints:
        reference = footprint.GetReference()
        value = footprint.GetValue()
        
        # Determine the category of the component
        category = "unknown"
        for cat_name, components in component_categories.items():
            for component in components:
                if component in value or component in reference:
                    category = cat_name
                    break
            if category != "unknown":
                break
        
        print(f"Processing {reference} - {value} (Category: {category})")
        
        # Handle the component based on its category
        if category == "A_non_mirrorable":
            # Reposition without mirroring
            # For now, just move it to a new position
            old_pos = footprint.GetPosition()
            new_pos = pcbnew.VECTOR2I(old_pos.x, old_pos.y + pcbnew.IU_PER_MM * 10)  # Move 10mm in Y direction
            footprint.SetPosition(new_pos)
        elif category == "B_mirrorable":
            # Mirror position and orientation
            footprint.Flip(pcbnew.VECTOR2I(0, 0), True)
        elif category == "C_position_critical":
            # Position according to BTX specification
            # This would require specific positioning logic for each component
            pass
    
    return board

def main():
    """Main function to convert the PCB from ATX to BTX form factor."""
    # Get the absolute path to the PCB file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    pcb_path = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    
    # Load the BTX conversion specification
    spec_path = os.path.join(script_dir, "btx_conversion_spec.json")
    with open(spec_path, 'r') as f:
        btx_specs = json.load(f)
    
    # Load the PCB file
    board = pcbnew.LoadBoard(pcb_path)
    print("PCB file loaded successfully")
    
    # Mirror the board outline
    board = mirror_board_outline(board)
    
    # Reposition components
    board = reposition_components(board, btx_specs["component_categories"])
    
    # Save the modified PCB file
    output_path = os.path.join(repo_dir, "Kicad", "neotron-pico-btx.kicad_pcb")
    board.Save(output_path)
    print(f"Modified PCB saved to {output_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
