#!/usr/bin/env python3
import os
import sys

# Analyze the PCB file structure
pcb_file = 'Kicad/neotron-pico.kicad_pcb'
file_size = os.path.getsize(pcb_file)
print(f'PCB file size: {file_size} bytes')

# Read the first few lines to understand the file structure
with open(pcb_file, 'r') as f:
    header = ''.join([f.readline() for _ in range(20)])
    print('PCB file header:')
    print(header)

# Count the number of components and other elements
component_count = 0
module_count = 0
with open(pcb_file, 'r') as f:
    for line in f:
        if '(module ' in line:
            module_count += 1
        if '(comp ' in line:
            component_count += 1

print(f'Module count: {module_count}')
print(f'Component count: {component_count}')
