# Component Classification for microBTX Conversion

## Category A: Non-mirrorable Components

These components cannot be mirrored but can be rotated and repositioned:

- **Raspberry Pi Pico**: Main processor module
- **STM32F031K6T6**: Board Management Controller
- **MCP23S17**: I/O Expander
- **TLV320AIC23BPW**: Audio Codec
- **TPD7S019**: VGA ESD Protection
- **THS7316**: Video Buffer
- **74HC138**: Decoder
- **DS1307Z+**: Real-Time Clock

## Category B: Mirrorable Components

These components can be mirrored in position and orientation:

- **Resistors**: All resistor networks and individual resistors
- **Capacitors**: All capacitor arrays and individual capacitors
- **Inductors**: Power inductors and ferrite beads
- **Diodes**: Signal diodes, protection diodes
- **LEDs**: Status indicators
- **Transistors**: Small-signal transistors

## Category C: Position-critical Components

These components must be positioned according to BTX specification:

- **DE15HD**: VGA connector
- **Audio Jacks**: Line in/out, microphone
- **SD Card Slot**: Storage interface
- **Expansion Slots**: Seven expansion slots
- **Mounting Holes**: Board attachment points
- **Power Connector**: DC input

## Thermal Considerations

- **High-power Components**: Positioned within SRM region
- **Passive Cooling**: Optimized component placement for natural convection
- **Heat Dissipation Paths**: Maintained through proper copper pour connectivity

## Signal Integrity Critical Paths

- **Video Signal Path**: Raspberry Pi Pico to VGA connector
- **Audio Signal Path**: Audio codec to audio jacks
- **Expansion Bus**: Signal integrity for expansion slots
- **Clock Distribution**: Clock signals to various components
