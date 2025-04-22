# Board Transformation Specification

## Board Dimensions

- Original microATX dimensions: 244 × 244 mm
- Target microBTX dimensions: 264 × 267 mm

## Mounting Holes

- SRM mounting holes: 111.76 × 55.79 mm

## Transformation Steps

1. Mirror the board outline horizontally
2. Adjust board dimensions to match microBTX specifications (264 × 267 mm)
3. Reposition mounting holes according to microBTX standards
4. Handle Category A components: Reposition without mirroring, rotate if necessary
5. Handle Category B components: Mirror position and orientation
6. Handle Category C components: Position according to BTX specification
7. Reroute traces to maintain signal integrity
8. Verify expansion slot orientation and connector accessibility
9. Validate signal integrity and trace routing
10. Check geometric soundness and layer intersections

## BTX Layout Characteristics

- BTX uses a mirrored ("left-handed") layout compared to ATX
- Components are arranged in a linear fashion from front to back for better airflow
- Critical components are positioned within the Support and Retention Module (SRM) region
- The SRM region is designed to provide the most efficient thermal dissipation path
- Vertical mounting of the motherboard on the left-hand side of the case
