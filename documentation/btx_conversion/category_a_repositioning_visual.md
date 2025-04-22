# Category A Component Repositioning Visual Guide

## Original Component Placement

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

## Repositioned Components in microBTX Layout

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

## Key Points for Category A Components

1. **No Mirroring**: Category A components (CPU, GPU, etc.) are not mirrored, only repositioned
2. **Orientation Preserved**: Original orientation is preserved to maintain pin compatibility
3. **SRM Placement**: Critical components like CPU are placed within the SRM region
4. **Expansion Slots**: Maintain original orientation to ensure cards face outward

## Implementation Notes

When repositioning Category A components:

1. Use KiCad's Move tool (M key) to reposition components
2. Use the Rotate tool (R key) to rotate components as needed
3. Verify component placement using the 3D viewer
4. Ensure critical components are placed within the SRM region
