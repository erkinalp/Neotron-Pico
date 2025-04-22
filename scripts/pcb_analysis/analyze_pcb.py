#!/usr/bin/env python3
"""
Script to analyze the Neotron-Pico PCB file structure.
"""
import os
import sys
import re
import json

def analyze_pcb_file(pcb_file_path):
    """Analyze the PCB file structure."""
    print(f"Analyzing PCB file: {pcb_file_path}")
    
    # Check if the file exists
    if not os.path.exists(pcb_file_path):
        print(f"Error: PCB file not found at {pcb_file_path}")
        return False
    
    # Get file size
    file_size = os.path.getsize(pcb_file_path)
    print(f"PCB file size: {file_size} bytes")
    
    # Read the PCB file
    try:
        with open(pcb_file_path, 'r') as f:
            pcb_content = f.read()
    except Exception as e:
        print(f"Error reading PCB file: {e}")
        return False
    
    # Extract basic information
    version_match = re.search(r'\(version\s+(\d+)\)', pcb_content)
    version = version_match.group(1) if version_match else "Unknown"
    
    generator_match = re.search(r'\(generator\s+(\w+)\)', pcb_content)
    generator = generator_match.group(1) if generator_match else "Unknown"
    
    # Extract layers
    layers_match = re.search(r'\(layers(.*?)\)', pcb_content, re.DOTALL)
    layers_text = layers_match.group(1) if layers_match else ""
    
    # Extract board outline
    edge_cuts_matches = re.findall(r'\(gr_line.*?\(layer\s+"Edge\.Cuts"\).*?\)', pcb_content, re.DOTALL)
    
    # Extract footprints
    footprint_matches = re.findall(r'\(footprint\s+"([^"]+)".*?\)', pcb_content)
    
    # Count components by type
    component_types = {}
    for footprint in footprint_matches:
        component_type = footprint.split(':')[0] if ':' in footprint else footprint
        component_types[component_type] = component_types.get(component_type, 0) + 1
    
    # Extract board dimensions
    x_coords = []
    y_coords = []
    for edge_cut in edge_cuts_matches:
        start_match = re.search(r'\(start\s+([\d.-]+)\s+([\d.-]+)\)', edge_cut)
        if start_match:
            x_coords.append(float(start_match.group(1)))
            y_coords.append(float(start_match.group(2)))
        
        end_match = re.search(r'\(end\s+([\d.-]+)\s+([\d.-]+)\)', edge_cut)
        if end_match:
            x_coords.append(float(end_match.group(1)))
            y_coords.append(float(end_match.group(2)))
    
    if x_coords and y_coords:
        width_mm = (max(x_coords) - min(x_coords)) / 1000000
        height_mm = (max(y_coords) - min(y_coords)) / 1000000
    else:
        width_mm = 0
        height_mm = 0
    
    # Create analysis report
    analysis = {
        "file_path": pcb_file_path,
        "file_size": file_size,
        "version": version,
        "generator": generator,
        "layers": layers_text.strip(),
        "board_dimensions": {
            "width_mm": width_mm,
            "height_mm": height_mm
        },
        "component_count": len(footprint_matches),
        "component_types": component_types,
        "edge_cuts_count": len(edge_cuts_matches)
    }
    
    # Save analysis to file
    analysis_file = os.path.join(os.path.dirname(os.path.dirname(pcb_file_path)), 
                                "documentation", "btx_conversion", "pcb_analysis.json")
    
    os.makedirs(os.path.dirname(analysis_file), exist_ok=True)
    
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Analysis saved to: {analysis_file}")
    
    # Create a human-readable report
    report_file = os.path.join(os.path.dirname(os.path.dirname(pcb_file_path)), 
                              "documentation", "btx_conversion", "pcb_analysis.md")
    
    with open(report_file, 'w') as f:
        f.write("# Neotron-Pico PCB Analysis\n\n")
        f.write(f"## Basic Information\n\n")
        f.write(f"- **File Path**: {pcb_file_path}\n")
        f.write(f"- **File Size**: {file_size} bytes\n")
        f.write(f"- **KiCad Version**: {version}\n")
        f.write(f"- **Generator**: {generator}\n\n")
        
        f.write(f"## Board Dimensions\n\n")
        f.write(f"- **Width**: {width_mm:.2f} mm\n")
        f.write(f"- **Height**: {height_mm:.2f} mm\n\n")
        
        f.write(f"## Component Statistics\n\n")
        f.write(f"- **Total Components**: {len(footprint_matches)}\n\n")
        f.write(f"### Component Types\n\n")
        for component_type, count in sorted(component_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{component_type}**: {count}\n")
        
        f.write(f"\n## Board Outline\n\n")
        f.write(f"- **Edge Cuts**: {len(edge_cuts_matches)}\n\n")
        
        f.write(f"## microBTX Conversion Notes\n\n")
        f.write(f"- **Original Dimensions**: {width_mm:.2f} mm × {height_mm:.2f} mm\n")
        f.write(f"- **Target Dimensions**: 264 mm × 267 mm\n\n")
        f.write(f"The conversion will involve mirroring the board outline and repositioning components according to microBTX specifications.\n")
    
    print(f"Report saved to: {report_file}")
    return True

def main():
    """Main function."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(os.path.dirname(script_dir))
    pcb_file_path = os.path.join(repo_dir, "Kicad", "neotron-pico.kicad_pcb")
    
    success = analyze_pcb_file(pcb_file_path)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
