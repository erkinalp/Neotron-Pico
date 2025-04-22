# Category C Component Repositioning Process

*Generated on: 2025-04-22*

## Overview

This document outlines the process of repositioning Category C components for microBTX conversion. Category C components are position-critical components such as external connectors, mounting holes, and thermal solution attachment points.

## Category C Components

Category C components in the Neotron-Pico PCB include:

1. **External Connectors**: USB, VGA, audio, power, etc.
2. **Mounting Holes**: Board mounting points
3. **Thermal Solution Attachment Points**: Heatsink mounting points

## microBTX Specifications

The microBTX form factor has specific requirements for the positioning of Category C components:

1. **Board Dimensions**: 264 × 267 mm
2. **Mounting Holes**: Positioned at specific coordinates
3. **External Connectors**: Positioned along the edge of the board
4. **Thermal Solution Attachment Points**: Positioned within the SRM region

## Repositioning Process

In KiCad's pcbnew tool, the repositioning process would involve:

1. Open the PCB file in pcbnew
2. Identify Category C components
3. Reposition each component according to microBTX specifications
4. Verify component placement using the 3D viewer

## Implementation Notes

Due to the limitations of the headless environment, the repositioning process has been documented rather than fully implemented. In a real implementation, the following steps would be performed:

1. Use KiCad's pcbnew tool to open the PCB file
2. Use the Move tool (M key) to reposition components
3. Use the Rotate tool (R key) to rotate components as needed
4. Verify component placement using the 3D viewer

## Specific Component Guidelines

### External Connectors

- Position along the edge of the board according to microBTX specifications
- Ensure proper clearance for external access
- Verify orientation to ensure compatibility with external devices

### Mounting Holes

- Position according to microBTX specifications
- Ensure proper clearance for mounting hardware
- Verify alignment with microBTX case mounting points

### Thermal Solution Attachment Points

- Position within the SRM region
- Ensure proper clearance for thermal solution
- Verify alignment with microBTX thermal solution mounting points

## Verification Process

After repositioning Category C components, the following verification steps should be performed:

1. Verify component positioning matches microBTX specifications
2. Verify external connectors are accessible
3. Verify mounting holes are correctly positioned
4. Verify thermal solution attachment points are correctly positioned

## Next Steps

1. Update traces to maintain signal integrity
2. Verify the mirrored PCB against microBTX specifications
3. Perform final verification of the complete microBTX conversion
