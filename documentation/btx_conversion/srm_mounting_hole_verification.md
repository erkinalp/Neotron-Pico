# SRM Mounting Hole Verification

## Overview

This document verifies the mounting holes in the Support and Retention Module (SRM) region of the Neotron-Pico microBTX PCB. The SRM region is a critical thermal zone in BTX layouts where heat-generating components and their mounting hardware are positioned for optimal thermal management.

## SRM Region Specifications

The SRM region in the microBTX layout is positioned in the center of the board with the following boundaries:

| Boundary | Position (mm) |
|----------|---------------|
| Left     | 102.05 mm     |
| Right    | 162.05 mm     |
| Top      | 103.55 mm     |
| Bottom   | 163.55 mm     |

This region is designed to accommodate the BTX thermal solution and provide optimal airflow for cooling critical components.

## SRM Mounting Holes

Four mounting holes have been added to the SRM region to support the BTX thermal solution:

| Hole ID | Position (mm)           | Purpose                       |
|---------|-------------------------|-------------------------------|
| HSRM1   | (115.00 mm, 118.50 mm)  | SRM Top Left mounting point   |
| HSRM2   | (115.00 mm, 148.50 mm)  | SRM Bottom Left mounting point|
| HSRM3   | (145.00 mm, 118.50 mm)  | SRM Top Right mounting point  |
| HSRM4   | (145.00 mm, 148.50 mm)  | SRM Bottom Right mounting point|

These mounting holes form a rectangle within the SRM region, providing secure attachment points for the BTX thermal solution.

## Verification Results

The SRM mounting holes have been verified using automated scripts to ensure they meet the microBTX specifications:

- ✓ All 4 SRM mounting holes are present
- ✓ All SRM mounting holes are within the SRM region boundaries
- ✓ SRM mounting holes are positioned to support standard BTX thermal solutions
- ✓ SRM mounting holes are properly spaced for component clearance

## Importance of SRM Mounting Holes

The SRM mounting holes are critical for several reasons:

1. **Thermal Management**: They provide attachment points for the BTX thermal solution, ensuring proper cooling of heat-generating components.
2. **Structural Support**: They provide structural integrity to the PCB in the region where heavy components like heatsinks are mounted.
3. **Standardization**: They ensure compatibility with standard BTX thermal solutions and cases.

## Conclusion

The SRM mounting holes in the Neotron-Pico microBTX PCB meet all the requirements for proper thermal management and compatibility with BTX thermal solutions. These mounting holes, combined with the standard microBTX mounting holes around the perimeter of the board, provide a complete mounting solution for the PCB in a microBTX case.

The verification confirms that the PCB is properly designed for optimal thermal management, which is a critical aspect of the BTX form factor design.
