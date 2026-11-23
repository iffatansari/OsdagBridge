"""Report charts generated from already-computed OsdagBridge results.

The functions in this module never recalculate structural demand or capacity;
they only summarize values present in the report payload.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any


def _number(value: Any) -> float | None:
    try:
        if value in (None, "", "N.A.", "N/A", "---"):
            return None
        return float(str(value).replace(",", "").split()[0])
    except (TypeError, ValueError, IndexError):
        return None


def _max_values(values) -> float | None:
    numbers = [n for n in (_number(v) for v in values) if n is not None]
    return max(numbers) if numbers else None


def utilization_values(output_dict: dict) -> dict[str, float]:
    """Return one governing UR per requested primary bridge component."""
    result: dict[str, float] = {}
    design = (output_dict or {}).get("design_results", {}) or {}
    girder_urs = []
    for name, data in (design.get("per_girder", {}) or {}).items():
        if str(name).startswith("EB"):
            continue
        girder_urs.extend((c or {}).get("dcr") for c in (data or {}).get("checks", []))
    value = _max_values(girder_urs)
    if value is not None:
        result["Steel Plate Girders"] = value

    deck = (output_dict or {}).get("deck_design_results", {}) or {}
    value = _max_values(v for k, v in deck.items() if str(k).lower().startswith("ur_"))
    if value is not None:
        result["Concrete Deck Slab"] = value

    try:
        from osdagbridge.core.bridge_types.plate_girder.results_data import _extract_osdag_summary
    except ModuleNotFoundError:
        def _extract_osdag_summary(raw):
            return raw if isinstance(raw, dict) else {}
    for key, label in (("crossbracing_design_results", "Cross Bracing"),
                       ("end_diaphragm_design_results", "End Diaphragms")):
        values = []
        for members in ((output_dict or {}).get(key, {}) or {}).values():
            for force_types in (members or {}).values() if isinstance(members, dict) else []:
                for raw in (force_types or {}).values() if isinstance(force_types, dict) else []:
                    try:
                        values.append(_extract_osdag_summary(raw or {}).get("efficiency"))
                    except (AttributeError, TypeError):
                        pass
        value = _max_values(values)
        if value is not None:
            result[label] = value
    return result


def _quantity_values(inputs: dict) -> dict[str, float]:
    """Extract MT quantities using the canonical BOQ output keys."""
    candidates = {
        "Girders": ("steel_girders_wt_total", "steel_girders_mt"),
        "Cross Bracing": ("bracing_top_wt_total", "bracing_bot_wt_total", "bracing_diag_wt_total", "cross_bracing_mt"),
        "End Diaphragms": ("end_diaphragm_wt_total", "end_diaphragms_mt"),
    }
    result = {}
    for label, keys in candidates.items():
        values = [_number(inputs.get(k)) for k in keys]
        values = [v for v in values if v is not None]
        if values:
            result[label] = sum(values)
    return result


def create_report_charts(output_dict: dict, inputs: dict, directory: str | Path) -> dict[str, str]:
    """Create PNG assets and return paths keyed by report figure name."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    ur = utilization_values(output_dict or {})
    if ur:
        labels, values = list(ur), list(ur.values())
        fig, ax = plt.subplots(figsize=(8.2, 4.3), dpi=180)
        colours = ["#C62828" if value > 1.0 else "#91B014" for value in values]
        bars = ax.bar(labels, values, color=colours, edgecolor="#405000", linewidth=0.7)
        ax.axhline(1.0, color="#C62828", linestyle="--", linewidth=1.4, label="UR = 1.0 limit")
        ax.set_ylabel("Utilization Ratio (Demand / Capacity)")
        ax.set_title("Overall Design Check — Governing Utilization Ratios", weight="bold")
        ax.set_ylim(0, max(1.15, max(values) * 1.2))
        ax.grid(axis="y", alpha=0.22)
        ax.legend(loc="upper right", frameon=False)
        ax.tick_params(axis="x", rotation=18)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{value:.2f}", ha="center", va="bottom", fontsize=8)
        fig.tight_layout()
        path = out / "utilization_summary.png"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        paths["utilization_summary"] = str(path)

    quantities = _quantity_values(inputs or {})
    if quantities:
        fig, ax = plt.subplots(figsize=(7.6, 4.0), dpi=180)
        labels, values = list(quantities), list(quantities.values())
        ax.bar(labels, values, color=["#91B014", "#4C72B0", "#F39C12"], edgecolor="#37474F")
        ax.set_ylabel("Quantity (MT)")
        ax.set_title("Structural Steel Material Quantities", weight="bold")
        ax.grid(axis="y", alpha=0.22)
        ax.tick_params(axis="x", rotation=15)
        fig.tight_layout()
        path = out / "steel_quantities.png"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        paths["steel_quantities"] = str(path)

    concrete = _number((inputs or {}).get("concrete_deck_vol_total"))
    rebar = _number((inputs or {}).get("rebar_deck_wt_total"))
    if concrete is not None or rebar is not None:
        labels, values = [], []
        if concrete is not None:
            labels.append("Concrete deck (m³)"); values.append(concrete)
        if rebar is not None:
            labels.append("Reinforcement (MT)"); values.append(rebar)
        fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=180)
        ax.bar(labels, values, color=["#90CAF9", "#EF9A9A"][:len(values)], edgecolor="#37474F")
        ax.set_ylabel("Reported quantity")
        ax.set_title("Concrete Volume and Reinforcement Weight", weight="bold")
        ax.grid(axis="y", alpha=0.22)
        fig.tight_layout()
        path = out / "concrete_reinforcement_quantities.png"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        paths["concrete_reinforcement_quantities"] = str(path)
    return paths
