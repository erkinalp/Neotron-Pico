# MicroBTX Conversion for Neotron-Pico

This PR implements a microBTX conversion for the Neotron-Pico project, transforming the ATX-compatible board into a microBTX-compatible layout.

## Changes

- Convert ATX-compatible board to microBTX form factor
- Mirror board outline to match microBTX specifications (264mm x 267mm)
- Reposition components according to category classification:
  - Category A (Non-mirrorable): Multi-pin ICs, expansion slots
  - Category B (Mirrorable): Passive components, two/three-terminal components
  - Category C (Position-critical): External connectors, mounting holes
- Maintain signal integrity and trace routing
- Add comprehensive documentation for the conversion process
- Include verification steps for expansion slots, signal integrity, and geometric soundness
- Ensure compatibility with microBTX cases and thermal solutions

## Documentation

The conversion process is thoroughly documented in the `documentation/btx_conversion/` directory, including:

- Conversion report
- Component classification
- Board outline mirroring
- Component repositioning
- Trace rerouting
- Verification steps
- Before/after comparison

## Implementation

The conversion was implemented using KiCad's Python API (pcbnew) to programmatically modify the PCB layout. The implementation follows Intel's microBTX form factor specifications, ensuring compatibility with standard microBTX cases and thermal solutions.

## Benefits

This conversion provides a usable passively cooled motherboard for users with BTX computers, offering a modern alternative for legacy BTX systems.

Link to Devin run: https://app.devin.ai/sessions/af37f65f8b784230b64b3ba3f0364de6

Requested by: Erkin Alp Güney (erkinalp9035@gmail.com)
