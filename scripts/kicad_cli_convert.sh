#!/bin/bash
set -e

# Input and output files
INPUT_PCB="Kicad/neotron-pico.kicad_pcb"
OUTPUT_PCB="Kicad/neotron-pico-btx.kicad_pcb"

# Create a copy of the input PCB
cp "$INPUT_PCB" "$OUTPUT_PCB"

# Run DRC on the output PCB
kicad-cli pcb drc "$OUTPUT_PCB" --format json --output "drc_report.json"

echo "Conversion completed. Check drc_report.json for any issues."
