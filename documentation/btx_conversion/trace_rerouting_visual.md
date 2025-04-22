# Trace Rerouting Visual Guide

## Original Trace Routing

```
+---------------------+
|                     |
|  +---+              |
|  |CPU|---+          |
|  +---+   |          |
|          |          |
|          v          |
|         +--------+  |
|         |  RAM   |  |
|         +--------+  |
|              |      |
|  +---+       |      |
|  |GPU|<------+      |
|  +---+              |
|                     |
+---------------------+
```

## Rerouted Traces in microBTX Layout

```
+---------------------+
|                     |
|              +---+  |
|              |CPU|  |
|              +---+  |
|                |    |
|                v    |
|  +--------+         |
|  |  RAM   |         |
|  +--------+         |
|       |             |
|       |      +---+  |
|       +----->|GPU|  |
|              +---+  |
|                     |
+---------------------+
```

## Key Points for Trace Rerouting

1. **High-frequency Traces**: Optimized to minimize length and crossings
2. **Critical Path Lengths**: Maintained to ensure proper timing
3. **Signal Crossings**: Minimized to reduce interference
4. **Power Delivery Paths**: Verified to ensure proper power distribution
5. **Ground Plane Integrity**: Maintained to ensure proper grounding

## Implementation Notes

When rerouting traces:

1. Avoid obscure trace shapes
2. Avoid layer intersections
3. Use vias for layer crossings
4. Maintain appropriate trace width
5. Ensure proper clearance between traces
