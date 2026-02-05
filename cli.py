from __future__ import annotations
import argparse
from .pipeline import run_pipeline

def main() -> None:
    p = argparse.ArgumentParser(description="Compute FCA Consumer Duty Outcome Gap Score and charts.")
    p.add_argument("--input", required=True, help="Path to FCA firm-level complaints workbook (xlsx).")
    p.add_argument("--outdir", default="outputs", help="Directory to write outputs.")
    p.add_argument("--config", default="config.yml", help="Path to config.yml.")
    args = p.parse_args()

    outputs = run_pipeline(args.input, args.outdir, config_path=args.config)
    print("Wrote outputs:")
    for k, v in outputs.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
