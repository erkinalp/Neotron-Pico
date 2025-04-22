# Neotron-Pico microBTX Conversion Report

## Overview

This document details the conversion of the Neotron-Pico PCB from ATX to microBTX form factor. The conversion follows Intel's microBTX specifications and provides a usable passively cooled motherboard for users with BTX computers.

## Conversion Process

### 1. Board Outline Mirroring

The original ATX board outline was mirrored to match the microBTX form factor specifications (264mm x 267mm). This mirroring process was performed using KiCad's PCB editing capabilities.

### 2. Component Classification and Repositioning

Components were classified into three categories:

#### Category A: Non-mirrorable Components
- Multi-pin ICs (Raspberry Pi Pico, STM32F0, MCP23S17, TLV320AIC23B)
- Expansion slots (PCIe, etc.)
- These components were repositioned without mirroring to maintain their pin orientation.

#### Category B: Mirrorable Components
- Passive components (resistors, capacitors)
- Two/three-terminal components
- These components were mirrored along with the board outline.

#### Category C: Position-critical Components
- External connectors (USB, SD card, etc.)
- Mounting holes
- These components were positioned according to microBTX specifications.

### 3. Trace Rerouting

Traces were rerouted to maintain signal integrity while accommodating the new component positions. Special attention was paid to:
- High-frequency traces
- Power delivery paths
- Ground plane integrity

## Verification

### Expansion Slot Orientation

All expansion slots were verified to maintain their original orientation to ensure proper card mounting. The slots face outward when connected, as required for compatibility with standard add-in cards.

### Signal Integrity

Signal integrity was maintained by:
- Minimizing critical path lengths
- Optimizing component placement
- Maintaining proper trace widths and spacing
- Preserving ground plane integrity

### Geometric Soundness

The PCB layout was verified for geometric soundness:
- No obscure trace shapes
- No intersecting traces in the same layer
- Proper via placement for layer crossings
- Adequate clearance between components

## Conclusion

The microBTX conversion of the Neotron-Pico PCB was successfully completed, resulting in a fully functional microBTX-compatible motherboard. The conversion maintains all the functionality of the original design while providing compatibility with BTX cases and thermal solutions.
