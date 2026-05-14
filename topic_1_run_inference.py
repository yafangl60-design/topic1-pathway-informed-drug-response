#!/usr/bin/env python3
"""Run Topic 1 inference from an existing trained model and aligned feature table.

Example:
  python scripts/topic_1_run_inference.py \
    --model results/topic_1/manuscript_candidate/prism_external/ElasticNet_gdsc_full_model.pkl \
    --feature-matrix data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_feature_matrix.csv \
    --sample-index data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_sample_index.csv \
    --output results/topic_1/inference/example_prism_elasticnet_predictions.csv

This helper performs prediction only. It does not train models or validate claims.
"""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path


def load_model(path: Path):
    try:
        with path.open("rb") as f:
            return pickle.load(f)
    except Exception:
        try:
            import joblib
            return joblib.load(path)
        except Exception as exc:
            raise RuntimeError(f"Could not load model {path}: {exc}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Topic 1 prediction with an existing trained model.")
    parser.add_argument("--model", required=True, help="Path to a trained .pkl/.joblib model.")
    parser.add_argument("--feature-matrix", required=True, help="CSV feature matrix containing sample_id plus model features.")
    parser.add_argument("--output", required=True, help="Output CSV for predictions.")
    parser.add_argument("--sample-index", default=None, help="Optional sample-index CSV to merge metadata into predictions.")
    parser.add_argument("--sample-id-column", default="sample_id", help="Sample identifier column name.")
    parser.add_argument("--model-name", default=None, help="Optional model name to record in output.")
    args = parser.parse_args()

    import pandas as pd

    model_path = Path(args.model)
    feature_path = Path(args.feature_matrix)
    output_path = Path(args.output)
    model = load_model(model_path)

    features = pd.read_csv(feature_path)
    if args.sample_id_column not in features.columns:
        raise ValueError(f"Missing sample id column: {args.sample_id_column}")
    sample_ids = features[args.sample_id_column].copy()

    if hasattr(model, "feature_names_in_"):
        needed = list(model.feature_names_in_)
        missing = [c for c in needed if c not in features.columns]
        if missing:
            raise ValueError(f"Feature matrix is missing {len(missing)} model-required features. First missing: {missing[:10]}")
        X = features[needed]
    else:
        X = features.drop(columns=[args.sample_id_column])
        # Drop obvious non-feature label columns if present.
        drop_cols = [c for c in X.columns if c.endswith("_not_final_result") or c in {"analysis_label", "response_value", "response_metric"}]
        if drop_cols:
            X = X.drop(columns=drop_cols)

    X = X.apply(pd.to_numeric, errors="coerce").fillna(0.0)
    preds = model.predict(X)

    out = pd.DataFrame(
        {
            args.sample_id_column: sample_ids,
            "prediction": preds,
            "model_name": args.model_name or model_path.stem,
            "prediction_note": "Predicted GDSC-scale response from existing trained model; interpret external datasets using ranking/correlation caveats.",
        }
    )
    if args.sample_index:
        meta = pd.read_csv(args.sample_index)
        if args.sample_id_column in meta.columns:
            out = meta.merge(out, on=args.sample_id_column, how="right")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    print(f"Wrote {len(out)} predictions to {output_path}")


if __name__ == "__main__":
    main()
