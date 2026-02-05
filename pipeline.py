from __future__ import annotations
import os
import yaml
from .io import load_fca_firm_level_workbook
from .scoring import compute_outcome_gap_scores
from .plots import plot_top_n_bar, plot_driver_heatmap, plot_scatter_volume_upheld

def run_pipeline(input_path: str, outdir: str, config_path: str = "config.yml") -> dict:
    os.makedirs(outdir, exist_ok=True)

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    product_col = cfg.get("product_column", "Banking and credit cards")
    weights = cfg.get("weights", None)
    backlog_ratio_max = float(cfg.get("caps", {}).get("backlog_ratio_max", 2.0))
    top_n = int(cfg.get("charts", {}).get("top_n", 15))

    raw = load_fca_firm_level_workbook(input_path, product_col=product_col)
    scored = compute_outcome_gap_scores(raw, backlog_ratio_max=backlog_ratio_max, weights=weights)

    csv_path = os.path.join(outdir, "outcome_gap_scores.csv")
    scored.sort_values("outcome_gap_score", ascending=False).to_csv(csv_path, index=False)

    bar_path = os.path.join(outdir, "outcome_gap_top15_bar.png")
    heat_path = os.path.join(outdir, "outcome_gap_top15_heatmap.png")
    scatter_path = os.path.join(outdir, "outcome_gap_scatter.png")

    plot_top_n_bar(scored, bar_path, top_n=top_n)
    plot_driver_heatmap(scored, heat_path, top_n=top_n)
    plot_scatter_volume_upheld(scored.dropna(subset=["closed","upheld_rate","outcome_gap_score"]), scatter_path)

    return {"csv": csv_path, "bar": bar_path, "heatmap": heat_path, "scatter": scatter_path}
