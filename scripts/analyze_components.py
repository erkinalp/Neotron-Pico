"""
Script to analyze and categorize components in the Neotron-Pico PCB.
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

def analyze_components(pcb_file):
    """Analyze components in the PCB file and categorize them."""
    print(f"Analyzing components in {pcb_file}...")
    
    board = pcbnew.LoadBoard(pcb_file)
    
    category_a = ["Pico", "STM32F0", "MCP23S17", "TLV320AIC23B", "TPD7S019", "THS7316", 
                 "74HC138", "DS1307Z+", "PCIe", "PCI_Express", "SD_Card_Det", "AMS1117", 
                 "STX-4335", "DC-DC"]
    category_b = ["Resistor", "Capacitor", "Inductor", "Diode", "LED", "Transistor", "Ferrite"]
    category_c = ["DE15HD", "Jack", "SD_Card", "Conn_", "MountingHole", "USB", "Power"]
    
    prefix_category_map = {
        # Category A: Non-mirrorable components
        "U": "A_non_mirrorable",  # ICs, processors, etc.
        
        # Category B: Mirrorable components
        "R": "B_mirrorable",      # Resistors
        "C": "B_mirrorable",      # Capacitors
        "L": "B_mirrorable",      # Inductors
        "FB": "B_mirrorable",     # Ferrite beads
        "D": "B_mirrorable",      # Diodes
        "Q": "B_mirrorable",      # Transistors
        "Y": "B_mirrorable",      # Crystals
        "BT": "B_mirrorable",     # Batteries
        "F": "B_mirrorable",      # Fuses
        "NT": "B_mirrorable",     # Net ties
        "TP": "B_mirrorable",     # Test points
        "SW": "B_mirrorable",     # Switches
        
        # Category C: Position-critical components
        "J": "C_position_critical",  # Connectors
        "H": "C_position_critical",  # Mounting holes
        
        # Other components
        "LOGO": "B_mirrorable",   # Logos (can be mirrored)
        "JP": "B_mirrorable"      # Jumpers
    }
    
    component_types = {}
    category_counts = {
        "A_non_mirrorable": 0,
        "B_mirrorable": 0,
        "C_position_critical": 0,
        "unknown": 0
    }
    
    detailed_components = {
        "A_non_mirrorable": [],
        "B_mirrorable": [],
        "C_position_critical": [],
        "unknown": []
    }
    
    for footprint in board.GetFootprints():
        reference = footprint.GetReference()
        value = footprint.GetValue()
        
        category = "unknown"
        for comp in category_a:
            if comp.lower() in value.lower() or comp.lower() in reference.lower():
                category = "A_non_mirrorable"
                break
        
        if category == "unknown":
            for comp in category_c:
                if comp.lower() in value.lower() or comp.lower() in reference.lower():
                    category = "C_position_critical"
                    break
        
        if category == "unknown":
            for comp in category_b:
                if comp.lower() in value.lower() or comp.lower() in reference.lower():
                    category = "B_mirrorable"
                    break
        
        if category == "unknown":
            ref_prefix = ''.join([c for c in reference if not c.isdigit()])
            if ref_prefix in prefix_category_map:
                category = prefix_category_map[ref_prefix]
        
        ref_prefix = ''.join([c for c in reference if not c.isdigit()])
        if ref_prefix not in component_types:
            component_types[ref_prefix] = {
                "count": 0,
                "examples": [],
                "default_category": prefix_category_map.get(ref_prefix, "unknown")
            }
        
        component_types[ref_prefix]["count"] += 1
        if len(component_types[ref_prefix]["examples"]) < 3:
            component_types[ref_prefix]["examples"].append(f"{reference}: {value}")
        
        category_counts[category] += 1
        
        detailed_components[category].append({
            "reference": reference,
            "value": value,
            "prefix": ref_prefix
        })
    
    print("\nComponent Category Summary:")
    for category, count in category_counts.items():
        print(f"{category}: {count} components")
    
    print("\nComponent Type Analysis:")
    for prefix, data in sorted(component_types.items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"{prefix}: {data['count']} components")
        print("  Examples:")
        for example in data["examples"]:
            print(f"    - {example}")
    
    report = {
        "category_counts": category_counts,
        "component_types": component_types,
        "detailed_components": detailed_components
    }
    
    return report

def update_classification_doc(report, doc_file):
    """Update the component classification documentation with detailed analysis."""
    print(f"Updating classification documentation: {doc_file}")
    
    with open(doc_file, 'r') as f:
        content = f.readlines()
    
    uncategorized_section = -1
    for i, line in enumerate(content):
        if "Uncategorized" in line and "Components" in line:
            uncategorized_section = i
            break
    
    if uncategorized_section == -1:
        for i, line in enumerate(content):
            if "## DRC Considerations" in line:
                uncategorized_section = i
                content.insert(i, "\n## Uncategorized Components\n\n")
                content.insert(i+1, "The following components were not explicitly categorized but were handled as mirrorable components:\n\n")
                break
    
    uncategorized = report["detailed_components"]["unknown"]
    by_prefix = {}
    for comp in uncategorized:
        prefix = comp["prefix"]
        if prefix not in by_prefix:
            by_prefix[prefix] = []
        by_prefix[prefix].append(comp)
    
    table_content = ["| Component Type | Count | Examples | Handling |\n",
                    "|----------------|-------|----------|----------|\n"]
    
    for prefix, comps in sorted(by_prefix.items(), key=lambda x: len(x[1]), reverse=True):
        if len(comps) > 0:
            examples = ", ".join([c["reference"] for c in comps[:3]])
            if len(comps) > 3:
                examples += ", ..."
            table_content.append(f"| {prefix} | {len(comps)} | {examples} | Mirrored position and orientation |\n")
    
    if uncategorized_section >= 0:
        insert_pos = uncategorized_section + 2
        while insert_pos < len(content) and not content[insert_pos].startswith("##"):
            insert_pos += 1
        
        content[uncategorized_section+2:insert_pos] = table_content
    
    with open(doc_file, 'w') as f:
        f.writelines(content)
    
    print("Classification documentation updated successfully")

def main():
    """Main function."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    
    pcb_file = os.path.join(repo_dir, "Kicad", "neotron-pico-btx.kicad_pcb")
    doc_file = os.path.join(repo_dir, "documentation", "btx_conversion", "component_classification.md")
    
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file not found: {pcb_file}")
        return 1
    
    if not os.path.exists(doc_file):
        print(f"Error: Documentation file not found: {doc_file}")
        return 1
    
    report = analyze_components(pcb_file)
    update_classification_doc(report, doc_file)
    
    report_file = os.path.join(repo_dir, "documentation", "btx_conversion", "component_analysis.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Detailed component analysis saved to: {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
