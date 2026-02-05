from __future__ import annotations
import pandas as pd

KEY_COLS = ["Firm Name", "Group", "Joint Reporting", "Reporting period"]

def _prep_sheet(df: pd.DataFrame, product_col: str, value_name: str) -> pd.DataFrame:
    cols = KEY_COLS + [product_col]
    out = df[cols].copy()
    out.rename(columns={product_col: value_name}, inplace=True)
    return out

def load_fca_firm_level_workbook(path: str, product_col: str = "Banking and credit cards") -> pd.DataFrame:
    """Load and merge the FCA firm-level complaints workbook into a single table for a product column.

    Expected sheet names:
      - Closed
      - Opened
      - Percentage upheld
      - Percentage within 3 days
      - Percentage after 3 days, within
    """
    closed = pd.read_excel(path, sheet_name="Closed")
    opened = pd.read_excel(path, sheet_name="Opened")
    upheld = pd.read_excel(path, sheet_name="Percentage upheld")
    within3 = pd.read_excel(path, sheet_name="Percentage within 3 days")
    after3 = pd.read_excel(path, sheet_name="Percentage after 3 days, within")

    a = _prep_sheet(closed, product_col, "closed")
    b = _prep_sheet(opened, product_col, "opened")
    c = _prep_sheet(upheld, product_col, "upheld_rate")
    d = _prep_sheet(within3, product_col, "pct_within_3days")
    e = _prep_sheet(after3, product_col, "pct_after3_within")

    out = a.merge(b, on=KEY_COLS, how="outer")\
           .merge(c, on=KEY_COLS, how="outer")\
           .merge(d, on=KEY_COLS, how="outer")\
           .merge(e, on=KEY_COLS, how="outer")

    for col in ["closed","opened","upheld_rate","pct_within_3days","pct_after3_within"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out
