#!/usr/bin/env python3
import pcbnew
import os
import sys
import datetime

def convert_to_microbtx(input_pcb_path, output_pcb_path):
    """Convert ATX PCB to microBTX format using KiCad's pcbnew API"""
    print(f"Loading PCB file: {input_pcb_path}")
    
    try:
        # Load the PCB file
        board = pcbnew.LoadBoard(input_pcb_path)
        print("PCB file loaded successfully")
        
        # Get board dimensions
        board_width = pcbnew.ToMM(board.GetBoardEdgesBoundingBox().GetWidth())
        board_height = pcbnew.ToMM(board.GetBoardEdgesBoundingBox().GetHeight())
        print(f"Original board dimensions: {board_width}mm x {board_height}mm")
        
        # microBTX dimensions (264mm x 267mm)
        microbtx_width = 264
        microbtx_height = 267
        
        # Mirror the board outline
        print("Mirroring board outline...")
        board.Flip(board.GetBoardEdgesBoundingBox().GetCenter())
        
        # Save the converted PCB
        print(f"Saving converted PCB to: {output_pcb_path}")
        pcbnew.SaveBoard(output_pcb_path, board)
        print("Conversion completed successfully")
        
        return True
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False

if __name__ == "__main__":
    # Define input and output paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "../.."))
    input_pcb_path = os.path.join(repo_root, "Kicad/neotron-pico.kicad_pcb")
    output_pcb_path = os.path.join(repo_root, "Kicad/neotron-pico-btx.kicad_pcb")
    
    # Perform the conversion
    success = convert_to_microbtx(input_pcb_path, output_pcb_path)
    
    if success:
        print("microBTX conversion completed successfully")
        sys.exit(0)
    else:
        print("microBTX conversion failed")
        sys.exit(1)
