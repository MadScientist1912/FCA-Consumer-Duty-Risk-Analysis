# FCA Consumer Duty – Outcome Gap Score (Foreseeable Harm Proxy)

This repo converts **FCA firm-level complaints returns** into a composite **Outcome Gap Score (0–100)** to help prioritise where customer outcomes may be deteriorating (a *proxy* for **foreseeable harm** under FCA Consumer Duty).

## Data
Place the FCA workbook in `data/` (example filename):
- `data/firm-level-complaints-data-2025-h1.xlsx`

> Tip: If you don't want to commit data to GitHub, keep `data/` local and add it to `.gitignore`.

## Method (Outcome Gap Score)
For each firm with data in the chosen product column (default: **Banking and credit cards**), we compute:

- **Scale:** log(1 + closed complaints)
- **% upheld:** higher can indicate poorer outcomes
- **Timeliness (≤3 days):** slower is worse
- **Timeliness (>3 days within timeframe):** slower is worse
- **Backlog pressure:** opened / closed (capped)

Each component is **min–max normalised across firms**, combined using weights in `config.yml`, and rescaled to **0–100**.

## Quickstart

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2) Run
```bash
python scripts/run_pipeline.py \
  --input data/firm-level-complaints-data-2025-h1.xlsx \
  --outdir outputs
```

Outputs:
- `outputs/outcome_gap_scores.csv`
- `outputs/outcome_gap_top15_bar.png`
- `outputs/outcome_gap_top15_heatmap.png`
- `outputs/outcome_gap_scatter.png`

### 3) Optional CLI
```bash
pip install -e .
outcome-gap --input data/firm-level-complaints-data-2025-h1.xlsx --outdir outputs
```

## Responsible use
- This is a **screening signal**, not a compliance verdict.
- Reporting windows and reporting structures can vary.
- The score is sensitive to **weights and normalisation**; tune `config.yml` to match your governance view.

## License
MIT (see `LICENSE`).
