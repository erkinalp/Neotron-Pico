# microBTX Specifications for Neotron-Pico Conversion

## Board Dimensions
- **microBTX**: 264 × 267 mm (10.4 × 10.5 in)
- **Original microATX**: 244 × 244 mm (9.6 × 9.6 in)

## Thermal Design Requirements
- BTX layout establishes a straighter path of airflow with fewer obstacles
- Components should be arranged in a linear fashion from front to back
- Critical components (CPU, chipsets) should be placed within the Support and Retention Module (SRM) region
- The SRM region is designed to provide the most efficient thermal dissipation path
- Vertical mounting of the motherboard on the left-hand side (mirrored layout compared to ATX)

## SRM (Support and Retention Module) Specifications
- 4 mounting holes with distances of 111.76 × 55.79 mm (4.4 × 2.275 in)
- Heat sink attached to the casing itself, not solely to the motherboard

## Connector Placement Guidelines
- External connectors must be positioned for accessibility in BTX cases
- BTX uses a mirrored ("left-handed") layout compared to ATX
- Expansion slots must maintain proper orientation for card mounting

## Component Handling Rules for Conversion
1. **Category A (Non-mirrorable)**: Multi-pin ICs, processors, expansion slots
   - No mirroring allowed
   - Rotations and repositioning possible
   - Original orientation must be preserved

2. **Category B (Mirrorable)**: Passive components, power regulation components
   - Mirror position and orientation
   - Can be freely repositioned

3. **Category C (Position-critical)**: External connectors, mounting holes
   - Position according to BTX specification
   - Must be accessible from the correct side of the case
