from __future__ import annotations
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_top_n_bar(df: pd.DataFrame, outpath: str, top_n: int = 15, label_col: str = "Firm Name") -> None:
    top = df.sort_values("outcome_gap_score", ascending=False).head(top_n)
    labels = top[label_col].astype(str).tolist()
    scores = top["outcome_gap_score"].to_numpy()

    plt.figure(figsize=(11, 6))
    plt.barh(range(len(labels))[::-1], scores[::-1])
    plt.yticks(range(len(labels))[::-1], [textwrap.shorten(x, width=40, placeholder="…") for x in labels[::-1]])
    plt.xlabel("Outcome Gap Score (0–100)")
    plt.title(f"Top {top_n} firms by Outcome Gap Score")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def plot_driver_heatmap(df: pd.DataFrame, outpath: str, top_n: int = 15, label_col: str = "Firm Name") -> None:
    top = df.sort_values("outcome_gap_score", ascending=False).head(top_n)
    comp_cols = ["volume_norm","upheld_norm","slow_3days_norm","slow_after3_norm","backlog_norm"]
    heat = top[comp_cols].to_numpy()

    plt.figure(figsize=(10, 5))
    plt.imshow(heat, aspect="auto")
    plt.colorbar(label="Normalised driver (0–1)")
    plt.yticks(range(len(top)), [textwrap.shorten(x, width=38, placeholder="…") for x in top[label_col].astype(str).tolist()])
    plt.xticks(range(len(comp_cols)), ["Volume","Upheld","Slow ≤3d","Slow >3d","Backlog"], rotation=30, ha="right")
    plt.title("Drivers of Outcome Gap Score (top cohort)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def plot_scatter_volume_upheld(df: pd.DataFrame, outpath: str) -> None:
    x = np.log1p(df["closed"])
    y = df["upheld_rate"]
    sizes = 20 + 3 * df["outcome_gap_score"].fillna(0)

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, s=sizes, alpha=0.6)
    plt.xlabel("log(1 + closed complaints)")
    plt.ylabel("% upheld")
    plt.title("Scale vs validity of complaints (marker size ∝ Outcome Gap Score)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
