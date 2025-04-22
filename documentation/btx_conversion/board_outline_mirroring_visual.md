# Board Outline Mirroring Visual Guide

## Original ATX Layout

```
+---------------------+
|                     |
|  +---+              |
|  |CPU|              |
|  +---+              |
|                     |
|         +--------+  |
|         |  RAM   |  |
|         +--------+  |
|                     |
|  +---+    +-----+  |
|  |GPU|    | I/O  |  |
|  +---+    +-----+  |
|                     |
+---------------------+
```

## Mirrored microBTX Layout

```
+---------------------+
|                     |
|              +---+  |
|              |CPU|  |
|              +---+  |
|                     |
|  +--------+         |
|  |  RAM   |         |
|  +--------+         |
|                     |
|  +-----+    +---+  |
|  | I/O  |    |GPU|  |
|  +-----+    +---+  |
|                     |
+---------------------+
```

## Key Differences

1. **Component Orientation**: The entire layout is mirrored along the Y-axis
2. **Thermal Design**: Optimized for linear airflow in BTX cases
3. **Mounting Points**: Adjusted to match microBTX specifications
4. **Dimensions**: Adjusted to 264 × 267 mm (microBTX standard)

## Implementation Notes

When mirroring the board outline:

1. Multi-pin components (CPU, GPU, etc.) cannot be mirrored but must be repositioned
2. Passive components can be mirrored
3. External connectors must be positioned according to microBTX specifications
4. Traces must be rerouted to maintain signal integrity
