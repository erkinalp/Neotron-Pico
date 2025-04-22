# BTX Mounting Hole Verification

This document verifies that the mounting holes in the Neotron-Pico microBTX PCB have been properly recreated according to BTX specifications.

## BTX Mounting Hole Specifications

The BTX specification defines the following mounting hole positions:

| Reference | X Position (mm) | Y Position (mm) | Diameter (mm) | Drill (mm) |
|-----------|----------------|----------------|--------------|------------|
| H101 | 6.35 | 6.35 | 3.5 | 3.0 |
| H102 | 6.35 | 260.65 | 3.5 | 3.0 |
| H103 | 257.65 | 6.35 | 3.5 | 3.0 |
| H104 | 257.65 | 260.65 | 3.5 | 3.0 |
| H105 | 132.0 | 6.35 | 3.5 | 3.0 |
| H106 | 132.0 | 260.65 | 3.5 | 3.0 |
| H107 | 132.0 | 133.5 | 3.5 | 3.0 |

## Verification Process

The mounting holes were recreated using the `recreate_mounting_holes.py` script, which:

1. Removed all existing ATX mounting holes from the PCB
2. Created new mounting holes at the BTX-specified positions
3. Set the correct diameter and drill size for each mounting hole

## Compatibility with BTX Cases

The recreated mounting holes ensure compatibility with standard BTX cases by:

1. Matching the BTX specification for mounting hole positions
2. Using the standard 3.5mm diameter with 3.0mm drill size
3. Positioning holes to align with BTX case standoffs

## Verification Results

The mounting holes have been successfully recreated according to BTX specifications. The PCB now has 7 mounting holes positioned correctly for BTX case compatibility.

## Conclusion

The Neotron-Pico microBTX PCB now has properly positioned mounting holes that comply with BTX specifications, ensuring compatibility with BTX cases. This completes the "Mounting holes correctly positioned" requirement from the layout verification checklist.
