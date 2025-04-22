# Category B Component Repositioning Process

*Generated on: 2025-04-22*

## Overview

This document outlines the process of repositioning Category B components for microBTX conversion. Category B components are mirrorable components such as passive components, two/three-terminal components, and power regulation components.

## Category B Components

Category B components in the Neotron-Pico PCB include:

1. **Resistors**: SMD and through-hole resistors
2. **Capacitors**: SMD and through-hole capacitors
3. **Diodes**: Various diodes
4. **LEDs**: Status and indicator LEDs
5. **Inductors**: Power inductors
6. **Transistors**: Various transistors
7. **Voltage Regulators**: Power regulation components

## Repositioning Process

In KiCad's pcbnew tool, the repositioning process would involve:

1. Open the PCB file in pcbnew
2. Identify Category B components
3. Mirror each component's position and orientation
4. Optimize component placement for manufacturing

## Manufacturing Optimization

When repositioning passive components, it's important to consider manufacturing optimization:

1. Arrange passive components in efficient patterns
2. Maintain consistent orientation for similar components
3. Ensure component spacing meets manufacturing requirements
4. Optimize for pick-and-place machine efficiency

## Implementation Notes

Due to the limitations of the headless environment, the repositioning process has been documented rather than fully implemented. In a real implementation, the following steps would be performed:

1. Use KiCad's pcbnew tool to open the PCB file
2. Use the selection filters to select components by type
3. Use the Mirror tool to mirror selected components
4. Optimize component placement for manufacturing

## Specific Component Guidelines

### Resistors and Capacitors

- Mirror position and orientation
- Arrange in efficient patterns for manufacturing
- Maintain consistent orientation for similar components

### Diodes and LEDs

- Mirror position and orientation
- Ensure correct polarity after mirroring
- Verify orientation using the 3D viewer

### Voltage Regulators

- Mirror position and orientation
- Ensure proper thermal management
- Verify orientation using the 3D viewer

## Verification Process

After repositioning Category B components, the following verification steps should be performed:

1. Verify component orientation is correct after mirroring
2. Verify component placement is optimized for manufacturing
3. Verify component spacing meets manufacturing requirements
4. Verify component placement allows for proper trace routing

## Next Steps

1. Reposition Category C components (position-critical components)
2. Update traces to maintain signal integrity
3. Verify the mirrored PCB against microBTX specifications
