# Component Classification for microBTX Conversion

## Overview

This document details the classification of components for the Neotron-Pico microBTX conversion. Components are categorized based on their handling requirements during the conversion process.

## Category A: Non-mirrorable Components

These components cannot be mirrored due to their pin orientation requirements:

| Component | Type | Handling |
|-----------|------|----------|
| Raspberry Pi Pico | Microcontroller | Repositioned without mirroring |
| STM32F0 | Microcontroller | Repositioned without mirroring |
| MCP23S17 | I/O Expander | Repositioned without mirroring |
| TLV320AIC23B | Audio Codec | Repositioned without mirroring |
| TPD7S019 | HDMI Interface | Repositioned without mirroring |
| THS7316 | Video Amplifier | Repositioned without mirroring |
| 74HC138 | Decoder | Repositioned without mirroring |
| DS1307Z+ | RTC | Repositioned without mirroring |
| PCIe Slots | Expansion Slot | Maintained original orientation |
| SD Card Slot | Card Slot | Maintained original orientation |

## Category B: Mirrorable Components

These components can be safely mirrored:

| Component Type | Handling |
|----------------|----------|
| Resistors | Mirrored position and orientation |
| Capacitors | Mirrored position and orientation |
| Inductors | Mirrored position and orientation |
| Diodes | Mirrored position and orientation |
| LEDs | Mirrored position and orientation |
| Transistors | Mirrored position and orientation |
| Ferrite Beads | Mirrored position and orientation |

## Category C: Position-critical Components

These components require specific positioning according to microBTX specifications:

| Component | Type | Positioning |
|-----------|------|-------------|
| DE15HD | VGA Connector | Positioned according to microBTX spec |
| Audio Jacks | External Connector | Positioned according to microBTX spec |
| SD Card | Card Slot | Positioned according to microBTX spec |
| USB Ports | External Connector | Positioned according to microBTX spec |
| Power Connector | External Connector | Positioned according to microBTX spec |
| Mounting Holes | Mechanical | Positioned according to microBTX spec |

## Implementation Statistics

The actual implementation resulted in the following component counts:

| Category | Count | Description |
|----------|-------|-------------|
| A_non_mirrorable | 8 | Components repositioned without mirroring |
| B_mirrorable | 6 | Components mirrored in position and orientation |
| C_position_critical | 25 | Components positioned according to microBTX specifications |
| Uncategorized | 203 | Components handled as mirrorable by default |

| Component Type | Count | Examples | Handling |
|----------------|-------|----------|----------|
| R | 96 | R809, R804, R811, ... | Mirrored position and orientation |
| C | 50 | C1301, C1302, C1202, ... | Mirrored position and orientation |
| NT | 12 | NT912, NT911, NT907, ... | Mirrored position and orientation |
| JP | 8 | JP201, JP1001, JP403, ... | Mirrored position and orientation |
| Q | 7 | Q1303, Q201, Q1302, ... | Mirrored position and orientation |
| TP | 6 | TP101, TP102, TP103, ... | Mirrored position and orientation |
| J | 5 | J903, J905, J902, ... | Mirrored position and orientation |
| U | 5 | U1302, U1301, U802, ... | Mirrored position and orientation |
| LOGO | 3 | LOGO103, LOGO102, LOGO101 | Mirrored position and orientation |
| FB | 2 | FB802, FB801 | Mirrored position and orientation |
| Y | 2 | Y1201, Y801 | Mirrored position and orientation |
| D | 2 | D1302, D1301 | Mirrored position and orientation |
| SW | 2 | SW1001, SW1002 | Mirrored position and orientation |
| BT | 1 | BT1201 | Mirrored position and orientation |
| F | 1 | F1301 | Mirrored position and orientation |
| L | 1 | L1301 | Mirrored position and orientation |
## DRC Considerations

Special attention was paid to component placement to avoid Design Rule Check (DRC) violations:

1. **Silkscreen Clipping**: Component silkscreen elements were adjusted to avoid clipping by solder mask
2. **Clearance Violations**: Minimum clearances were enforced between components and traces
3. **Track Width Violations**: Minimum track widths were enforced for all traces
4. **Via Size and Drill Violations**: Minimum via dimensions were enforced for all vias

These considerations ensure that the PCB meets manufacturing requirements while maintaining the proper component categorization and handling.
