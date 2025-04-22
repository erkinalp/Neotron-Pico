# microBTX Conversion for Neotron-Pico

## Overview

This directory contains documentation and scripts for converting the Neotron-Pico PCB from ATX to microBTX form factor. The conversion follows Intel's microBTX specifications and aims to provide a passively cooled motherboard for users with BTX computers.

## Specifications

- **Original Form Factor**: microATX (244 × 244 mm)
- **Target Form Factor**: microBTX (264 × 267 mm)
- **Thermal Design**: Passive cooling with optimized component placement
- **Layer Stack-up**: Preserved from original design

## Conversion Process

The conversion process involves:

1. Mirroring the board outline
2. Repositioning components based on their category:
   - Category A (Non-mirrorable): Multi-pin ICs, processors
   - Category B (Mirrorable): Passive components
   - Category C (Position-critical): External connectors, mounting holes
3. Rerouting traces to maintain signal integrity
4. Verifying expansion slot orientation and connector accessibility

## Verification Checklist

- Board dimensions match microBTX specification
- Component orientations correct per category
- Expansion slots properly oriented
- External connectors accessible
- Mounting holes correctly positioned
- Signal integrity maintained
- Manufacturing requirements met

## Implementation

The conversion is implemented using KiCad's pcbnew Python API. See the scripts directory for the implementation details.
