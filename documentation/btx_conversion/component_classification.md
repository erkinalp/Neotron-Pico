# Component Classification for microBTX Conversion

## Category A: Non-mirrorable Components

These components cannot be mirrored due to their pin orientation requirements:

| Component | Type | Handling |
|-----------|------|----------|
| Raspberry Pi Pico | Microcontroller | Repositioned without mirroring |
| STM32F0 | Microcontroller | Repositioned without mirroring |
| MCP23S17 | I/O Expander | Repositioned without mirroring |
| TLV320AIC23B | Audio Codec | Repositioned without mirroring |
| PCIe Slots | Expansion Slot | Maintained original orientation |
| SD Card Slot | Card Slot | Maintained original orientation |

## Category B: Mirrorable Components

These components can be safely mirrored:

| Component Type | Count | Handling |
|----------------|-------|----------|
| Resistors | 127 | Mirrored position and orientation |
| Capacitors | 89 | Mirrored position and orientation |
| Diodes | 18 | Mirrored position and orientation |
| Transistors | 7 | Mirrored position and orientation |
| Ferrite Beads | 5 | Mirrored position and orientation |

## Category C: Position-critical Components

These components require specific positioning according to microBTX specifications:

| Component | Type | Positioning |
|-----------|------|-------------|
| USB Ports | External Connector | Positioned according to microBTX spec |
| Audio Jacks | External Connector | Positioned according to microBTX spec |
| Video Output | External Connector | Positioned according to microBTX spec |
| Power Connector | External Connector | Positioned according to microBTX spec |
| Mounting Holes | Mechanical | Positioned according to microBTX spec |
