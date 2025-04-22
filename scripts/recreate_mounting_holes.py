"""
Script to recreate mounting holes according to BTX specifications.
"""
import sys
import os
import json
sys.path.append('/usr/lib/python3/dist-packages')

try:
    import pcbnew
except ImportError:
    print("Error: pcbnew module not found. Make sure KiCad is installed.")
    sys.exit(1)

def recreate_mounting_holes(pcb_file, specs_file, output_file=None):
    """Recreate mounting holes according to BTX specifications."""
    print(f"Loading PCB file: {pcb_file}")
    board = pcbnew.LoadBoard(pcb_file)
    
    with open(specs_file, 'r') as f:
        btx_specs = json.load(f)
    
    mounting_holes = []
    for footprint in board.GetFootprints():
        if footprint.GetReference().startswith('H'):
            mounting_holes.append(footprint)
    
    print(f"Removing {len(mounting_holes)} existing mounting holes")
    for hole in mounting_holes:
        board.Remove(hole)
    
    print(f"Creating {len(btx_specs['mounting_holes'])} new mounting holes")
    KICAD_UNIT_MM = 1000000
    
    for hole_spec in btx_specs['mounting_holes']:
        x_pos = int(hole_spec['x'] * KICAD_UNIT_MM)
        y_pos = int(hole_spec['y'] * KICAD_UNIT_MM)
        position = pcbnew.VECTOR2I(x_pos, y_pos)
        
        module_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "Kicad", "MountingHole.pretty", "MountingHole_3.2mm_M3.kicad_mod")
        
        if not os.path.exists(module_path):
            new_hole = pcbnew.FOOTPRINT(board)
            board.Add(new_hole)
            new_hole.SetReference(hole_spec['reference'])
            new_hole.SetValue("MountingHole")
            new_hole.SetPosition(position)
            
            pad = pcbnew.PAD(new_hole)
            new_hole.Add(pad)
            pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
            
            diameter = int(hole_spec['diameter'] * KICAD_UNIT_MM)
            drill = int(hole_spec['drill'] * KICAD_UNIT_MM)
            pad.SetSize(pcbnew.VECTOR2I(diameter, diameter))
            pad.SetDrillSize(pcbnew.VECTOR2I(drill, drill))
            pad.SetNumber("1")
            
            pad.SetLayerSet(pcbnew.LSET.AllCuMask())
        else:
            new_hole = pcbnew.FootprintLoad(os.path.dirname(module_path), 
                                           os.path.basename(module_path))
            new_hole.SetReference(hole_spec['reference'])
            new_hole.SetPosition(position)
            board.Add(new_hole)
    
    if output_file is None:
        output_file = pcb_file
    
    print(f"Saving modified PCB to: {output_file}")
    board.Save(output_file)
    return True

def main():
    """Main function."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    
    pcb_file = os.path.join(repo_dir, "Kicad", "neotron-pico-btx.kicad_pcb")
    specs_file = os.path.join(script_dir, "btx_specs", "mounting_holes.json")
    
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file not found: {pcb_file}")
        return 1
    
    if not os.path.exists(specs_file):
        print(f"Error: Specifications file not found: {specs_file}")
        return 1
    
    success = recreate_mounting_holes(pcb_file, specs_file)
    
    if success:
        print("Successfully recreated mounting holes according to BTX specifications")
        return 0
    else:
        print("Failed to recreate mounting holes")
        return 1

if __name__ == "__main__":
    sys.exit(main())
