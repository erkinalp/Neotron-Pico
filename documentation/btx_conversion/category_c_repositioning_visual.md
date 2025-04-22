# Category C Component Repositioning Visual Guide

## Original External Connector Placement

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
 | | | |  | | | | | |
 U V A P  U U U S P
 S G u o  S S S e o
 B A d w  B B B r w
       e        i e
       r        a r
                l
```

## Repositioned External Connectors in microBTX Layout

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
 | | | |  | | | | | |
 P S U U  U P A V U
 o e S S  S o u G S
 w r B B  B w d A B
 e i         e
 r a         r
   l
```

## Mounting Hole Placement

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

## Key Points for Category C Components

1. **External Connectors**: Positioned along the edge of the board according to microBTX specifications
2. **Mounting Holes**: Positioned at specific coordinates according to microBTX specifications
3. **Thermal Solution Attachment Points**: Positioned within the SRM region
4. **Accessibility**: External connectors are positioned for easy access

## Implementation Notes

When repositioning Category C components:

1. Use KiCad's Move tool (M key) to reposition components
2. Verify component placement using the 3D viewer
3. Ensure external connectors are accessible
4. Verify mounting holes are correctly positioned
