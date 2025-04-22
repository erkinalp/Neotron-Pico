# Neotron-Pico Component Classification for microBTX Conversion

## Category A: Non-mirrorable components
- **Raspberry Pi Pico** (Main CPU)
- **STM32F031K6T6** (Board Management Controller)
- **MCP23S17** (GPIO Expander)
- **TLV320AIC23BPW** (Audio CODEC)
- **THS7316** (Video Amplifier)
- **TPD7S019** (Video ESD Filter)
- **DS1307Z+** (Real Time Clock)
- **74HC138** (Decoder)

## Category B: Mirrorable components
- **Passive components** (resistors, capacitors) - "Jellybeans" in 0805 package
- **Transistors** (SOT-23)
- **K7805-3AR3** (Power Supply)

## Category C: Position-critical components
- **DE15 VGA connector** (External video output)
- **Audio connectors** (Line in/out, headphone, microphone)
- **Expansion slots** (Multiple slots for peripherals)
- **Test headers** (For debugging and testing)
- **Mounting holes** (For securing the board to the case)

## Thermal Considerations
- The Neotron-Pico is described as "perfectly suitable for passive cooling" and "low power"
- In BTX layout, components should be arranged in a linear fashion from front to back for better airflow
- Critical components (Raspberry Pi Pico, STM32F0) should be placed within the Support and Retention Module (SRM) region
- The SRM region is designed to provide the most efficient thermal dissipation path

## Signal Integrity Critical Paths
- **VGA output signals** - High-frequency signals requiring careful routing
- **Digital audio signals** - Between the Audio CODEC and connectors
- **SPI bus** - Communication between Raspberry Pi Pico and peripherals
- **Expansion slot signals** - Must maintain proper orientation and signal integrity
