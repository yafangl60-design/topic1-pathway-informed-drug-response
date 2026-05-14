# Topic 1 Inference Script

The inference helper is `scripts/topic_1_run_inference.py`. It loads an existing trained model and an aligned feature matrix, then writes predictions. It does not train models, tune hyperparameters, rerun validation, or make clinical claims.

## Available Local Model Files

- `results/topic_1/manuscript_candidate/prism_external/ElasticNet_gdsc_full_model.pkl`
- `results/topic_1/manuscript_candidate/prism_external/ProposedV1_GroupedElasticNet_gdsc_full_model.pkl`
- `results/topic_1/manuscript_candidate/prism_external/RandomForest_gdsc_full_model.pkl`
- `results/topic_1/manuscript_candidate/prism_external/Ridge_gdsc_full_model.pkl`
- `results/topic_1/manuscript_candidate/prism_external/XGBoost_gdsc_full_model.pkl`

## Example: PRISM Candidate Prediction

```bash
python scripts/topic_1_run_inference.py \
  --model results/topic_1/manuscript_candidate/prism_external/ElasticNet_gdsc_full_model.pkl \
  --feature-matrix data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_feature_matrix.csv \
  --sample-index data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_sample_index.csv \
  --output results/topic_1/inference/example_prism_elasticnet_predictions.csv
```

## Interpretation Boundary

- Predictions from GDSC-trained models are on the learned GDSC response scale.
- PRISM LFC is a different response scale; PRISM use should remain ranking/correlation-oriented candidate validation.
- The script is for reproducibility and reviewer inspection, not clinical use.