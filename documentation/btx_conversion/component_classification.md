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
| A_non_mirrorable | 16 | Components repositioned without mirroring |
| B_mirrorable | 176 | Components mirrored in position and orientation |
| C_position_critical | 50 | Components positioned according to microBTX specifications |

### Category A: Non-mirrorable Components (16)

These components were repositioned without mirroring to maintain pin orientation:

| Component Type | Count | Examples | Handling |
|----------------|-------|----------|----------|
| U (ICs) | 13 | U201 (Pico), U1001 (STM32F0), U1302 (AMS1117-3.3) | Repositioned without mirroring, rotated 180° if needed |
| LOGO | 3 | LOGO103, LOGO102, LOGO101 | Repositioned without mirroring to maintain proper appearance |

### Category B: Mirrorable Components (179)

These components were mirrored in both position and orientation:

| Component Type | Count | Examples | Handling |
|----------------|-------|----------|----------|
| R (Resistors) | 96 | R809, R804, R811 | Mirrored position and orientation |
| C (Capacitors) | 50 | C1301, C1302, C1202 | Mirrored position and orientation |
| NT (Net Ties) | 12 | NT912, NT911, NT907 | Mirrored position and orientation |
| Q (Transistors) | 7 | Q1303, Q201, Q1302 | Mirrored position and orientation |
| TP (Test Points) | 6 | TP101, TP102, TP103 | Mirrored position and orientation |

| FB (Ferrite Beads) | 2 | FB802, FB801 | Mirrored position and orientation |
| Y (Crystals) | 2 | Y1201, Y801 | Mirrored position and orientation |
| D (Diodes) | 2 | D1302, D1301 | Mirrored position and orientation |
| SW (Switches) | 2 | SW1001, SW1002 | Mirrored position and orientation |
| BT (Batteries) | 1 | BT1201 | Mirrored position and orientation |
| F (Fuses) | 1 | F1301 | Mirrored position and orientation |
| L (Inductors) | 1 | L1301 | Mirrored position and orientation |

### Category C: Position-critical Components (50)

These components were positioned according to microBTX specifications:

| Component Type | Count | Examples | Handling |
|----------------|-------|----------|----------|
| J (Connectors) | 23 | J903 (Expansion Slot), J803 (Conn_01x04) | Positioned according to microBTX spec |
| H (Mounting Holes) | 7 | H101, H105, H102 | Recreated according to microBTX spec (ATX mounting holes don't correspond to BTX positions) |
| JP (Jumpers) | 8 | JP201, JP1001, JP403 | Positioned according to microBTX spec |
| SD Card Slot | 1 | SD Card | Positioned according to microBTX spec |
| VGA Connector | 1 | DE15HD | Positioned according to microBTX spec |
| Audio Jacks | 2 | Audio In/Out | Positioned according to microBTX spec |
| USB Ports | 2 | USB | Positioned according to microBTX spec |
| Power Connector | 1 | Power | Positioned according to microBTX spec |
## DRC Considerations

Special attention was paid to component placement to avoid Design Rule Check (DRC) violations:

1. **Silkscreen Clipping**: Component silkscreen elements were adjusted to avoid clipping by solder mask
2. **Clearance Violations**: Minimum clearances were enforced between components and traces
3. **Track Width Violations**: Minimum track widths were enforced for all traces
4. **Via Size and Drill Violations**: Minimum via dimensions were enforced for all vias

These considerations ensure that the PCB meets manufacturing requirements while maintaining the proper component categorization and handling.
