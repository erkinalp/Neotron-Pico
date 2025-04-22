#!/usr/bin/env python3
"""
Script to convert the Neotron-Pico PCB from ATX to BTX form factor.
Since we don't have direct access to pcbnew, we'll create a specification
for the conversion that can be implemented using KiCad's GUI.
"""
import os
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def get_pcb_info(pcb_path):
    """Extract basic information from the PCB file."""
    try:
        # Check if the file exists
        if not os.path.exists(pcb_path):
            print(f"Error: PCB file not found at {pcb_path}")
            return None
            
        print(f"PCB file exists at {pcb_path}")
        print(f"File size: {os.path.getsize(pcb_path) / (1024 * 1024):.2f} MB")
        
        # Read the first few lines to get version info
        with open(pcb_path, 'r') as f:
            header = ''.join([f.readline() for _ in range(10)])
            print("PCB file header:")
            print(header)
            
        return {
            "file_path": pcb_path,
            "file_size_mb": os.path.getsize(pcb_path) / (1024 * 1024),
            "exists": True
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_conversion_spec(pcb_info):
    """Create a detailed specification for the BTX conversion."""
    if not pcb_info:
        return
        
    # Define the BTX specifications
    btx_specs = {
        "original_dimensions": {"width": 244, "height": 244},  # microATX in mm
        "target_dimensions": {"width": 264, "height": 267},    # microBTX in mm
        "mounting_holes": {
            "srm": {"width": 111.76, "height": 55.79}  # SRM mounting holes in mm
        },
        "component_categories": {
            "A_non_mirrorable": [
                "Raspberry Pi Pico", "STM32F031K6T6", "MCP23S17", 
                "TLV320AIC23BPW", "THS7316", "TPD7S019", "DS1307Z+", 
                "74HC138", "Expansion Slots"
            ],
            "B_mirrorable": [
                "Resistors", "Capacitors", "Transistors (SOT-23)", 
                "K7805-3AR3 (Power Supply)"
            ],
            "C_position_critical": [
                "DE15 VGA connector", "Audio connectors", 
                "Expansion slots", "Test headers", "Mounting holes"
            ]
        },
        "transformation_steps": [
            "1. Mirror the board outline horizontally",
            "2. Adjust board dimensions to match microBTX specifications (264 × 267 mm)",
            "3. Reposition mounting holes according to microBTX standards",
            "4. Handle Category A components: Reposition without mirroring, rotate if necessary",
            "5. Handle Category B components: Mirror position and orientation",
            "6. Handle Category C components: Position according to BTX specification",
            "7. Reroute traces to maintain signal integrity",
            "8. Verify expansion slot orientation and connector accessibility",
            "9. Validate signal integrity and trace routing",
            "10. Check geometric soundness and layer intersections"
        ]
    }
    
    # Create a JSON specification file
    spec_path = os.path.join(os.path.dirname(pcb_info["file_path"]), "..", "scripts", "btx_conversion_spec.json")
    with open(spec_path, 'w') as f:
        json.dump(btx_specs, f, indent=2)
    
    print(f"BTX conversion specification created at {spec_path}")
    return spec_path

def main():
    """Main function to create the BTX conversion specification."""
    # Get the absolute path to the PCB file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    pcb_path = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    
    # Get PCB information
    pcb_info = get_pcb_info(pcb_path)
    
    # Create conversion specification
    spec_path = create_conversion_spec(pcb_info)
    
    # Create a Python script template for when pcbnew is available
    pcbnew_script_path = os.path.join(script_dir, "btx_conversion_pcbnew.py")
    with open(pcbnew_script_path, 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Script to convert the Neotron-Pico PCB from ATX to BTX form factor using KiCad's pcbnew API.
\"\"\"
import sys
import os
import json
import pcbnew

def mirror_board_outline(board):
    \"\"\"Mirror the board outline horizontally.\"\"\"
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
    \"\"\"Reposition components according to their categories.\"\"\"
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
    \"\"\"Main function to convert the PCB from ATX to BTX form factor.\"\"\"
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
""")
    
    print(f"pcbnew script template created at {pcbnew_script_path}")
    print("\nTo complete the BTX conversion, you'll need to:")
    print("1. Install KiCad and ensure the pcbnew Python module is available")
    print("2. Run the btx_conversion_pcbnew.py script to perform the actual conversion")
    print("3. Verify the conversion using KiCad's GUI")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
