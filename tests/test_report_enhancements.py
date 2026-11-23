import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from osdagbridge.core.reports.chap3 import ch3_loads
from osdagbridge.core.reports.report_generator import _ensure_longtable_headers
from osdagbridge.core.reports.visualizations import utilization_values, create_report_charts
from osdagbridge.core.utils.common import (
    KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_FOOTPATH_PRESSURE_VALUE,
    KEY_LL_IRC_CLASS_A,
    KEY_LL_IRC_CLASS_SV,
    KEY_SPAN,
)


def test_vehicle_and_footway_tables_are_separate_and_repeat_headers():
    values = {
        KEY_LL_IRC_CLASS_A: True,
        KEY_LL_IRC_CLASS_SV: True,
        KEY_SPAN: 20,
        KEY_LL_FOOTPATH_PRESSURE_MODE: "Custom",
        KEY_LL_FOOTPATH_PRESSURE_VALUE: 3.0,
    }
    tex = ch3_loads(values)
    assert "Vehicle Live Loads (LL)" in tex
    assert "Footway Live Load" in tex
    assert tex.count(r"\begin{longtable}") >= 6
    assert r"\endfirsthead" in tex and r"\endhead" in tex


def test_utilization_summary_uses_governing_component_values():
    output = {
        "design_results": {"per_girder": {"G1": {"checks": [{"dcr": 0.82}]}}},
        "deck_design_results": {"ur_flexure": 1.08},
    }
    assert utilization_values(output) == {
        "Steel Plate Girders": 0.82,
        "Concrete Deck Slab": 1.08,
    }


def test_chart_assets_are_written_to_requested_directory(tmp_path):
    paths = create_report_charts(
        {"design_results": {"per_girder": {"G1": {"checks": [{"dcr": 0.82}]}}}},
        {
            "steel_girders_wt_total": 12.5,
            "concrete_deck_vol_total": 40,
            "rebar_deck_wt_total": 2.3,
        },
        tmp_path,
    )
    assert {"utilization_summary", "steel_quantities", "concrete_reinforcement_quantities"} <= paths.keys()
    assert all(Path(path).exists() for path in paths.values())


def test_longtable_postprocessor_adds_continuation_header():
    tex = """\\begin{longtable}{|c|c|}
\\hline
\\textbf{A} & \\textbf{B} \\\\
\\hline
1 & 2 \\\\
\\end{longtable}"""
    enhanced = _ensure_longtable_headers(tex)
    assert r"\endfirsthead" in enhanced
    assert r"\endhead" in enhanced
