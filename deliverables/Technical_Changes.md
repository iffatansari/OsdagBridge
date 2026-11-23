# OsdagBridge LaTeX Report Generator — Technical Changes

## Executive summary

The report generator was refactored around a single report-theme module, data-driven chart generation, and explicit longtable continuation headers. The implementation keeps structural calculations in the existing analysis/design pipeline and limits the reporting layer to formatting, extraction, and visualization of already-computed values.

## Files changed under the report generator

- `src/osdagbridge/core/reports/styles.py` — new centralized theme containing page geometry, colours, table padding, row spacing, footer clearance, and global LaTeX layout controls.
- `src/osdagbridge/core/reports/visualizations.py` — new Matplotlib chart factory for governing utilization ratios and material quantities. It writes temporary PNG assets during report generation and returns paths for PyLaTeX/LaTeX figure embedding.
- `src/osdagbridge/core/reports/report_generator.py` — orchestration changes: chart asset creation, BOQ-before-chart ordering, longtable header post-processing, safer page geometry, and insertion of the Chapter 5/7 figures.
- `src/osdagbridge/core/reports/chap3.py` — vehicle live loads and footway pressure are now rendered as separate tables. Vehicle rows follow the live-load checkboxes/custom vehicle data supplied by the UI and include impact, braking, and eccentricity columns with units.
- `src/osdagbridge/core/reports/chap5.py` — signature remains backward-compatible while the orchestrator injects the utilization summary figure after the overall design-check table.
- `src/osdagbridge/core/reports/chap7.py` — signature remains backward-compatible while the orchestrator injects material quantity figures after the bill of materials.
- `tests/test_report_enhancements.py` — focused tests for table separation, repeated headers, governing UR extraction, and chart asset creation.
- `tools/generate_report_examples.py` — deterministic fixture used to compile the requested baseline and enhanced example PDFs without requiring a GUI session.

## Longtable and footer-overlap strategy

Existing report tables already use `longtable` in most chapters. The orchestration layer now scans assembled report TeX and adds `\\endfirsthead` and `\\endhead` blocks to longtables with bold column headings. This causes the headings to repeat automatically on every continued page. Chapter 3 additionally declares continuation headers directly because its live-load tables are generated dynamically.

The page geometry provides explicit header/footer clearance, while `\\needspace` guards the beginning of normal and long tables. Consistent `\\tabcolsep`, `\\arraystretch`, `\\extrarowheight`, and `\\LTpre`/`\\LTpost` values reduce cramped rows and keep the final rows away from the footer region. The approach avoids arbitrary manual page breaks that could create empty pages when input data changes.

## Load and geometry refactor

The former merged Live Loads table obscured the difference between vehicles and footway pressure. The new layout contains:

1. **Vehicle Live Loads (LL):** vehicle class, total load, impact factor, braking load, and eccentricity.
2. **Footway Live Load:** pressure value, application mode, and code/unit basis.

Vehicle labels are derived from the canonical UI keys (`Class A`, `70R`, `AA`, `SV`, fatigue, and custom vehicles). The report therefore reflects the user's selected loading-tab inputs instead of displaying a static example.

## Utilization-ratio visualization

`visualizations.utilization_values()` reads the maximum demand/capacity ratio already stored by the design pipeline for:

- Steel plate girders
- Concrete deck slab
- Cross bracing
- End diaphragms

`create_report_charts()` creates a professional bar chart, colours passing/failing bars differently, labels values, and adds the mandatory red dashed `UR = 1.0` reference line. The chart is saved under the report's temporary image directory and embedded after the Chapter 5 overall design-check summary.

## Material quantity visualization

The quantity chart reads the same BOQ values used by Chapter 7. It generates one chart for structural steel tonnage by component and a second chart comparing concrete deck volume with reinforcement steel weight. BOQ quantities are calculated before chart creation, ensuring that the table and figures cannot drift apart.

## Centralized style system

`styles.py` is the single source of truth for:

- A4 geometry and footer/headroom constraints
- Osdag green, pass/fail, header-fill, and border colours
- Body font size and line spacing
- Table cell padding and row height
- Longtable spacing and page-bottom guard thresholds

The report generator imports this configuration rather than introducing a second theme. Chapter modules remain focused on content and consume shared helpers for escaping and figure construction.

## Validation performed

- Python compilation checks passed for all changed report modules.
- Focused tests cover live-load table structure, chart values/assets, and longtable continuation headers.
- `tools/generate_report_examples.py` produces `Report_Before.pdf` and `Report_After.pdf` with `pdflatex` for visual comparison.
- The enhanced report uses temporary image assets, so generated output directories do not accumulate stale chart files.

## Repository submission note

The implementation is prepared in the local clone of `Nidhikhare12/OsdagBridge` on the `dev` branch. A GitHub fork URL and collaborator invitation require an authenticated GitHub account with permission to create the fork and invite `Nidhikhare12`; those account-level actions should be completed from the student's GitHub session before final submission.
