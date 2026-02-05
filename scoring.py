from __future__ import annotations
import numpy as np
import pandas as pd

def _minmax(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    mn = np.nanmin(s.values)
    mx = np.nanmax(s.values)
    if np.isfinite(mn) and np.isfinite(mx) and mx > mn:
        return (s - mn) / (mx - mn)
    return pd.Series(np.zeros(len(s)), index=series.index)

def compute_outcome_gap_scores(
    df: pd.DataFrame,
    backlog_ratio_max: float = 2.0,
    weights: dict | None = None,
) -> pd.DataFrame:
    """Compute Outcome Gap Score (0-100) and normalised drivers."""
    w = weights or {
        "volume_log_closed": 0.35,
        "upheld_rate": 0.25,
        "slow_within_3days": 0.15,
        "slow_after3_within_timeframe": 0.15,
        "backlog_ratio_capped": 0.10,
    }

    out = df.copy()
    out["backlog_ratio"] = out["opened"] / out["closed"]
    out["log_closed"] = np.log1p(out["closed"])
    out["slow_3days"] = 1 - out["pct_within_3days"]
    out["slow_after3"] = 1 - out["pct_after3_within"]
    out["backlog_ratio_capped"] = out["backlog_ratio"].clip(lower=0, upper=backlog_ratio_max)

    out["volume_norm"] = _minmax(out["log_closed"])
    out["upheld_norm"] = _minmax(out["upheld_rate"])
    out["slow_3days_norm"] = _minmax(out["slow_3days"])
    out["slow_after3_norm"] = _minmax(out["slow_after3"])
    out["backlog_norm"] = _minmax(out["backlog_ratio_capped"])

    score = (
        w["volume_log_closed"] * out["volume_norm"]
        + w["upheld_rate"] * out["upheld_norm"]
        + w["slow_within_3days"] * out["slow_3days_norm"]
        + w["slow_after3_within_timeframe"] * out["slow_after3_norm"]
        + w["backlog_ratio_capped"] * out["backlog_norm"]
    )
    out["outcome_gap_score"] = 100 * score
    return out
