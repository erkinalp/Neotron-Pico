# Layout Verification Against microBTX Specifications Visual Guide

## microBTX Board Dimensions

```
+---------------------+
|                     |
|                     |
|                     |
|                     |
|                     |
|                     |
|                     |
|                     |
+---------------------+
264 × 267 mm
```

## Mounting Hole Positions

```
+---------------------+
| O               O  |
|                    |
|                    |
|                    |
|                    |
|                    |
|                    |
| O               O  |
+---------------------+
```

## Component Orientation

```
Category A (Non-mirrorable):
+-----+
|     |
|     |
|     |
+-----+

Category B (Mirrorable):
+---+
|   |
+---+

Category C (Position-critical):
+-----+
|     |
|     |
+-----+
```

## Key Points for Layout Verification

1. **Board Dimensions**: 264 × 267 mm
2. **Mounting Hole Positions**:
   - (111.76 mm, 55.79 mm)
   - (111.76 mm, 211.21 mm)
   - (152.24 mm, 55.79 mm)
   - (152.24 mm, 211.21 mm)
3. **Component Orientations**:
   - Category A: No mirroring, rotations and repositioning possible
   - Category B: Mirror position and orientation
   - Category C: Position according to microBTX specification
4. **Expansion Slot Orientation**: Maintain original orientation
5. **External Connector Accessibility**: Position along the edge of the board
6. **Thermal Solution Attachment Points**: Position within the SRM region

## Implementation Notes

When verifying the layout against microBTX specifications:

1. Use KiCad's 3D viewer to verify board dimensions
2. Use KiCad's 3D viewer to verify mounting hole positions
3. Use KiCad's 3D viewer to verify component orientations
4. Use KiCad's 3D viewer to verify expansion slot orientation
5. Use KiCad's 3D viewer to verify external connector accessibility
6. Use KiCad's 3D viewer to verify thermal solution attachment points
