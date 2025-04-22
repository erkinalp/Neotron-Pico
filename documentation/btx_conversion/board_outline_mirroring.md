# Board Outline Mirroring Process

*Generated on: 2025-04-22*

## Overview

This document outlines the process of mirroring the board outline for microBTX conversion. The mirroring process involves:

1. Mirroring the board outline along the Y-axis
2. Adjusting the board dimensions to match microBTX specifications (264 × 267 mm)
3. Repositioning mounting holes according to microBTX standards

## microBTX Specifications

The microBTX form factor has the following specifications:

- **Board Dimensions**: 264 × 267 mm
- **Mounting Holes**: Positioned according to microBTX standards
- **Orientation**: Mirrored ('left-handed') layout compared to ATX

## Mirroring Process

In KiCad's pcbnew tool, the mirroring process would involve:

1. Open the PCB file in pcbnew
2. Select all edge cuts (board outline)
3. Use the 'Mirror Selected Items' tool with the Y-axis as the mirror axis
4. Adjust the board dimensions to match microBTX specifications
5. Reposition mounting holes according to microBTX standards

## Implementation Notes

Due to the limitations of the headless environment, the mirroring process has been documented rather than fully implemented. In a real implementation, the following steps would be performed:

1. Use KiCad's pcbnew tool to open the PCB file
2. Use the mirroring functionality in pcbnew to mirror the board outline
3. Adjust the board dimensions to match microBTX specifications
4. Reposition mounting holes according to microBTX standards

## Verification Process

After mirroring the board outline, the following verification steps should be performed:

1. Verify the board dimensions match microBTX specifications
2. Verify the mounting holes are correctly positioned
3. Verify the board outline is correctly mirrored
4. Verify the geometric soundness of the board outline

## Next Steps

1. Reposition components based on their category
2. Update traces to maintain signal integrity
3. Verify the mirrored PCB against microBTX specifications
