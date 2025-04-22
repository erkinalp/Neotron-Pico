# microBTX Specifications

## Form Factor Dimensions

- **microBTX**: 264 × 267 mm
- **Original microATX**: 244 × 244 mm

## Mounting Hole Positions

The microBTX form factor uses a different mounting hole pattern compared to ATX:

- Standard mounting hole spacing: 111.76 × 55.79 mm
- Holes positioned to align with BTX case standoffs

## Thermal Design

BTX was designed with a linear airflow pattern:

1. Air enters at the front of the case
2. Flows over the Support and Retention Module (SRM) region
3. Exits at the rear of the case

Even for passively cooled systems, component placement should follow BTX thermal zones:

- High-power components placed in the SRM region
- Thermal-sensitive components positioned for optimal passive cooling

## Component Placement Guidelines

### Category A: Non-mirrorable Components

- Multi-pin ICs (Raspberry Pi Pico, STM32F0, etc.)
- Processors and complex integrated circuits
- Expansion slots

These components cannot be mirrored but can be rotated and repositioned.

### Category B: Mirrorable Components

- Passive components (resistors, capacitors)
- Two/three-terminal components
- Power regulation components

These components can be mirrored in position and orientation.

### Category C: Position-critical Components

- External connectors (VGA, audio jacks, etc.)
- Mounting holes
- Thermal solution attachment points

These components must be positioned according to BTX specification for proper case compatibility.

## Signal Integrity Considerations

- Preserve high-frequency trace lengths
- Minimize signal crossings
- Maintain power delivery paths
- Ensure ground plane integrity

## Manufacturing Optimization

- Arrange passive components in efficient patterns
- Maintain component spacing requirements
- Preserve layer stack-up
- Maintain copper pour connectivity
- Verify thermal relief settings
