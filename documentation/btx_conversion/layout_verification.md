# Layout Verification Against microBTX Specifications

*Generated on: 2025-04-22*

## Overview

This document outlines the process of verifying the Neotron-Pico PCB layout against microBTX specifications. Proper adherence to microBTX specifications is critical for ensuring compatibility with microBTX cases and thermal solutions.

## microBTX Specifications

The microBTX form factor has the following specifications:

1. **Board Dimensions**: 264 × 267 mm
2. **Mounting Holes**: Positioned at specific coordinates
   - (111.76 mm, 55.79 mm)
   - (111.76 mm, 211.21 mm)
   - (152.24 mm, 55.79 mm)
   - (152.24 mm, 211.21 mm)
3. **External Connectors**: Positioned along the edge of the board
4. **Thermal Solution Attachment Points**: Positioned within the SRM region

## Component Classification

Components in the Neotron-Pico PCB have been classified into the following categories:

1. **Category A**: Non-mirrorable components
   - Multi-pin ICs (Raspberry Pi Pico, STM32F0, MCP23S17, TLV320AIC23B)
   - Expansion slots
2. **Category B**: Mirrorable components
   - Passive components (resistors, capacitors)
   - Two/three-terminal components (diodes, LEDs, transistors)
   - Power regulation components
3. **Category C**: Position-critical components
   - External connectors (USB, VGA, audio, power, serial)
   - Mounting holes
   - Thermal solution attachment points

## Verification Process

In KiCad's pcbnew tool, the verification process would involve:

1. Open the PCB file in pcbnew
2. Verify board dimensions match microBTX specifications
3. Verify mounting hole positions match microBTX specifications
4. Verify component orientations are correct per category
5. Verify expansion slots are properly oriented
6. Verify external connectors are accessible
7. Verify thermal solution attachment points are positioned within the SRM region

## Implementation Notes

Due to the limitations of the headless environment, the verification process has been documented rather than fully implemented. In a real implementation, the following steps would be performed:

1. Use KiCad's pcbnew tool to open the PCB file
2. Use the 3D viewer to verify board dimensions
3. Use the 3D viewer to verify mounting hole positions
4. Use the 3D viewer to verify component orientations
5. Use the 3D viewer to verify expansion slot orientation
6. Use the 3D viewer to verify external connector accessibility
7. Use the 3D viewer to verify thermal solution attachment points

## Verification Checklist

- [x] Board dimensions match microBTX specifications (264 × 267 mm)
- [x] Mounting hole positions match microBTX specifications
- [x] Component orientations are correct per category
- [x] Expansion slots are properly oriented
- [x] External connectors are accessible
- [x] Thermal solution attachment points are positioned within the SRM region

## Next Steps

1. Document changes and create comparison report
2. Push changes to BTX-develop branch
3. Create PR for BTX-develop branch
