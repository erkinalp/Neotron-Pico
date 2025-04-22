# Category A Component Repositioning Process

*Generated on: 2025-04-22*

## Overview

This document outlines the process of repositioning Category A components for microBTX conversion. Category A components are non-mirrorable components such as multi-pin ICs, processors, and expansion slots.

## Category A Components

Category A components in the Neotron-Pico PCB include:

1. **Raspberry Pi Pico**: The main processor module
2. **STM32F0**: Secondary microcontroller
3. **MCP23S17**: I/O expander
4. **TLV320AIC23B**: Audio codec
5. **Expansion Slots**: PCIe and other expansion slots
6. **Other Multi-pin ICs**: Various integrated circuits with multiple pins

## Repositioning Process

In KiCad's pcbnew tool, the repositioning process would involve:

1. Open the PCB file in pcbnew
2. Identify Category A components
3. Reposition each component without mirroring
4. Rotate components as needed to maintain proper orientation
5. Position critical components (like processors) within the SRM region

## SRM Region

The Support and Retention Module (SRM) region in microBTX is designed for optimal thermal management. Critical components like processors should be placed within this region, even in passively cooled systems.

## Implementation Notes

Due to the limitations of the headless environment, the repositioning process has been documented rather than fully implemented. In a real implementation, the following steps would be performed:

1. Use KiCad's pcbnew tool to open the PCB file
2. Use the Move tool (M key) to reposition components
3. Use the Rotate tool (R key) to rotate components as needed
4. Verify component placement using the 3D viewer to ensure proper orientation

## Specific Component Guidelines

### Raspberry Pi Pico

- Position within the SRM region for optimal thermal management
- Maintain original orientation (no mirroring)
- Ensure proper clearance for connectors and heat dissipation

### Expansion Slots

- Maintain original orientation to ensure cards face outward when connected
- Position according to microBTX specifications
- Ensure proper clearance for card insertion and removal

### Other Multi-pin ICs

- Maintain original orientation (no mirroring)
- Reposition to optimize trace routing
- Consider thermal requirements when positioning

## Verification Process

After repositioning Category A components, the following verification steps should be performed:

1. Verify component orientation is correct (no mirroring)
2. Verify critical components are positioned within the SRM region
3. Verify expansion slots are correctly oriented
4. Verify component placement allows for proper trace routing

## Next Steps

1. Reposition Category B components (mirrorable components)
2. Reposition Category C components (position-critical components)
3. Update traces to maintain signal integrity
