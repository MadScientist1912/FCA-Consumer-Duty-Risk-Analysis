from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Allow running without installing package
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from outcome_gap.pipeline import run_pipeline

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--outdir", default="outputs")
    p.add_argument("--config", default="config.yml")
    args = p.parse_args()
    run_pipeline(args.input, args.outdir, config_path=args.config)

if __name__ == "__main__":
    main()
