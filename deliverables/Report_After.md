# OsdagBridge Design Report — Enhanced Output

**Report version:** Refactored layout and visualization pipeline  
**Status rule:** UR ≤ 1.0 = passing; UR > 1.0 = failing

## Loads and Load Combinations

### Vehicle Live Loads (LL)

| Vehicle class | Total load (kN) | Impact factor | Braking load | Eccentricity (m) |
|---|---:|---:|---:|---:|
| Class A | — | 1.25 | 83.4 | 1.20 |
| Class SV | — | 1.25 | 83.4 | 1.20 |

### Footway Live Load

| Parameter | Value | Basis / unit |
|---|---:|---|
| Footway pressure | 3.0 | kN/m²; IRC 6 Cl. 206.1 or user-defined |
| Application | Uniformly distributed | Footpath / footway area |

## Overall Design Check Summary

![Governing utilization ratios](assets/utilization_summary.png)

The chart is generated from the governing demand/capacity values already computed by the design pipeline. The red dashed line is the mandatory UR = 1.0 threshold.

## Material Take-off and Quantity Summary

![Structural steel quantities](assets/steel_quantities.png)

![Concrete and reinforcement quantities](assets/concrete_reinforcement_quantities.png)

The figures use the same BOQ quantities as the Chapter 7 table and are saved as temporary image assets during report generation.

## Layout and style improvements

- Longtables repeat their column headings on continued pages.
- Page geometry, row height, cell padding, and footer clearance are centralized in `styles.py`.
- Vehicle and footway loads are separated into clear unit-aware tables.
- Passing and failing utilization bars are visually distinguished.
