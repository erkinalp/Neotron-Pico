# Neotron-Pico microBTX Conversion Specification

## Board Transformation Requirements

### 1. Board Outline Mirroring
- Original microATX dimensions: 244 × 244 mm
- Target microBTX dimensions: 264 × 267 mm
- The board outline must be mirrored horizontally to create a "left-handed" layout
- Mounting holes must be positioned according to microBTX specifications

### 2. Component Handling Rules

#### Category A: Non-mirrorable components
- **No mirroring allowed** - These components must maintain their original orientation
- Rotations and repositioning are permitted
- Components in this category:
  - Raspberry Pi Pico (Main CPU)
  - STM32F031K6T6 (Board Management Controller)
  - MCP23S17 (GPIO Expander)
  - TLV320AIC23BPW (Audio CODEC)
  - THS7316 (Video Amplifier)
  - TPD7S019 (Video ESD Filter)
  - DS1307Z+ (Real Time Clock)
  - 74HC138 (Decoder)
  - All expansion slots

#### Category B: Mirrorable components
- **Mirror position and orientation**
- Can be freely repositioned
- Components in this category:
  - Passive components (resistors, capacitors)
  - Transistors (SOT-23)
  - K7805-3AR3 (Power Supply)

#### Category C: Position-critical components
- **Position according to BTX specification**
- Must be accessible from the correct side of the case
- Components in this category:
  - DE15 VGA connector
  - Audio connectors
  - Expansion slots
  - Test headers
  - Mounting holes

### 3. Trace Routing Guidelines
- Board layout and traces should be mirrored while preserving the original orientation of multi-terminal components
- Expansion slot orientation must be preserved to ensure cards face outward when connected
- Signal integrity must be maintained for high-frequency traces (VGA, audio)
- Minimize trace crossings, particularly for high-frequency signals

### 4. SRM (Support and Retention Module) Integration
- 4 mounting holes with distances of 111.76 × 55.79 mm (4.4 × 2.275 in)
- Critical components (Raspberry Pi Pico, STM32F0) should be placed within the SRM region
- The SRM region is designed for optimal thermal dissipation

## Visual Transformation Guide

```
Original ATX Layout:
+---------------------------+
|                           |
|  [CPU]                    |
|                           |
|  [Slots]                  |
|                           |
|  [I/O Ports]              |
+---------------------------+

Mirrored BTX Layout:
+---------------------------+
|                           |
|                    [CPU]  |
|                           |
|                  [Slots]  |
|                           |
|              [I/O Ports]  |
+---------------------------+
```

## Implementation Notes
- The entire board layout must be rearranged to maintain compatibility with BTX cases
- Special attention must be paid to component-specific mirroring rules
- Thermal management is critical - components should be arranged in a linear fashion from front to back
- External connectors must be positioned for accessibility in BTX cases
