
import os
import sys
import json
import pcbnew
import math

def load_btx_specs(specs_path):
    """Load the BTX conversion specifications."""
    with open(specs_path, 'r') as f:
        return json.load(f)

def determine_component_category(footprint, btx_specs):
    """Determine the category of a component based on its reference and value."""
    reference = footprint.GetReference()
    value = footprint.GetValue()
    
    # Check Category A (Non-mirrorable)
    for component in btx_specs["component_categories"]["A_non_mirrorable"]:
        if component.lower() in value.lower() or component.lower() in reference.lower():
            return "A_non_mirrorable"
    
    # Check Category C (Position-critical)
    for component in btx_specs["component_categories"]["C_position_critical"]:
        if component.lower() in value.lower() or component.lower() in reference.lower():
            return "C_position_critical"
    
    # Check Category B (Mirrorable)
    for component in btx_specs["component_categories"]["B_mirrorable"]:
        if component.lower() in value.lower() or component.lower() in reference.lower():
            return "B_mirrorable"
    
    # Default to unknown
    return "unknown"

def convert_pcb(pcb_path, output_path, btx_specs):
    """Convert the PCB file from ATX to BTX form factor using pcbnew."""
    print(f"Converting PCB file: {pcb_path}")
    print(f"Output file: {output_path}")
    
    # Load the PCB file
    board = pcbnew.LoadBoard(pcb_path)
    
    # Get the board dimensions
    board_width = btx_specs["target_dimensions"]["width"] * 1000000  # Convert to internal units (nm)
    
    # Process all footprints
    for footprint in board.GetFootprints():
        # Get the current position
        position = footprint.GetPosition()
        x = position.x
        y = position.y
        
        # Determine the category of the component
        category = determine_component_category(footprint, btx_specs)
        reference = footprint.GetReference()
        value = footprint.GetValue()
        
        print(f"Processing {reference} - {value} (Category: {category})")
        
        # Handle the component based on its category
        if category == "A_non_mirrorable":
            # Reposition without mirroring
            new_x = board_width - x
            new_y = y
            
            # Create new position
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
            
        elif category == "B_mirrorable":
            # Mirror position and orientation
            new_x = board_width - x
            new_y = y
            
            # Create new position
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
            
            # Flip the orientation
            orientation = footprint.GetOrientation()
            new_orientation = orientation + 180 * 10  # KiCad uses decidegrees (1/10 of a degree)
            footprint.SetOrientation(new_orientation)
            
        elif category == "C_position_critical":
            # Position according to BTX specification
            new_x = board_width - x
            new_y = y
            
            # Create new position
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
            
        else:
            # Unknown category, just mirror the position
            new_x = board_width - x
            new_y = y
            
            # Create new position
            new_position = pcbnew.VECTOR2I(int(new_x), int(new_y))
            footprint.SetPosition(new_position)
    
    # Mirror the board outline
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcbnew.Edge_Cuts:
            # Get the current position
            start_x = drawing.GetStart().x
            start_y = drawing.GetStart().y
            end_x = drawing.GetEnd().x
            end_y = drawing.GetEnd().y
            
            # Mirror the position
            new_start_x = board_width - start_x
            new_start_y = start_y
            new_end_x = board_width - end_x
            new_end_y = end_y
            
            # Set the new position
            drawing.SetStart(pcbnew.VECTOR2I(int(new_start_x), int(new_start_y)))
            drawing.SetEnd(pcbnew.VECTOR2I(int(new_end_x), int(new_end_y)))
    
    # Save the modified PCB file
    pcbnew.SaveBoard(output_path, board)
    
    print("PCB file converted successfully")
    return True

def main():
    """Main function to convert the PCB from ATX to BTX form factor."""
    if len(sys.argv) < 4:
        print("Usage: python3 convert_pcb.py <pcb_path> <output_path> <specs_path>")
        return 1
    
    pcb_path = sys.argv[1]
    output_path = sys.argv[2]
    specs_path = sys.argv[3]
    
    # Load the BTX conversion specifications
    btx_specs = load_btx_specs(specs_path)
    
    # Convert the PCB file
    success = convert_pcb(pcb_path, output_path, btx_specs)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
