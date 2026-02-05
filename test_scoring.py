import pandas as pd
from outcome_gap.scoring import compute_outcome_gap_scores

def test_score_range():
    df = pd.DataFrame({
        "closed":[100,200],
        "opened":[110,150],
        "upheld_rate":[0.2,0.5],
        "pct_within_3days":[0.5,0.9],
        "pct_after3_within":[0.6,0.8],
    })
    out = compute_outcome_gap_scores(df)
    assert out["outcome_gap_score"].between(0, 100).all()
