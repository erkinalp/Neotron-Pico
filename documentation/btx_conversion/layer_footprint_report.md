# Layer Footprint Verification Report

## Overview

This document reports the results of layer footprint verification for the Neotron-Pico microBTX PCB conversion.

## Board Information

- Board dimensions: 264.10 mm x 267.10 mm
- Copper layer count: 4
- Total footprints: 244
- Total copper zones: 7

## Layer Information

| Layer ID | Layer Name | Footprint Count | Zone Count |
|----------|------------|-----------------|------------|
| 0 | F.Cu | 238 | 4 |
| 1 | F.Mask | 0 | 0 |
| 2 | B.Cu | 6 | 1 |
| 3 | B.Mask | 0 | 0 |
| 4 | In1.Cu | 0 | 1 |
| 5 | F.Silkscreen | 0 | 0 |
| 6 | In2.Cu | 0 | 1 |
| 7 | B.Silkscreen | 0 | 0 |
| 9 | F.Adhesive | 0 | 0 |
| 11 | B.Adhesive | 0 | 0 |
| 13 | F.Paste | 0 | 0 |
| 15 | B.Paste | 0 | 0 |
| 17 | User.Drawings | 0 | 0 |
| 19 | User.Comments | 0 | 0 |
| 21 | User.Eco1 | 0 | 0 |
| 23 | User.Eco2 | 0 | 0 |
| 25 | Edge.Cuts | 0 | 0 |
| 27 | Margin | 0 | 0 |
| 29 | B.Courtyard | 0 | 0 |
| 31 | F.Courtyard | 0 | 0 |
| 33 | B.Fab | 0 | 0 |
| 35 | F.Fab | 0 | 0 |

## Footprint Verification

✅ All 244 footprints are within board outline.

## Zone Verification

❌ 4 zones extend beyond board outline:

| Layer | Min X (mm) | Min Y (mm) | Max X (mm) | Max Y (mm) |
|-------|------------|------------|------------|------------|
| F.Cu | 261.62 | 160.66 | 266.38 | 180.66 |
| B.Cu | 25.40 | 25.40 | 269.24 | 196.85 |
| In1.Cu | 25.40 | 25.40 | 269.24 | 196.85 |
| In2.Cu | 25.40 | 25.40 | 269.24 | 196.85 |

## Conclusion

❌ The PCB has layer footprint issues that need to be addressed.

### Recommended Actions

2. Adjust copper zones to match the board outline.
