# Topic 1 Cleaned Data Structure

This document describes the cleaned/frozen data objects used by the manuscript. It is repository documentation, not a replacement for the original third-party data sources.

## Frozen Data Files

| file | rows | columns | key columns |
| --- | --- | --- | --- |
| `data/frozen/topic_1_v3_baseline_20260505/topic_1_multiomics_feature_matrix_v3.csv` | 5000 | 1933 | sample_id, internal_baseline_dryrun_not_final_result, pathway_mean__Signal_Transduction, pathway_mean__Metabolism, pathway_mean__Immune_System, pathway_mean__Metabolism_of_proteins, pathway_mean__Disease, pathway_mean__Gene_expression_Transcription_ |
| `data/frozen/topic_1_v3_baseline_20260505/topic_1_multiomics_feature_metadata_v3.csv` | 1934 | 7 | feature_name, feature_group, source, is_placeholder, used_in_v2, source_file, notes |
| `data/frozen/topic_1_v3_baseline_20260505/topic_1_multiomics_sample_index_v3.csv` | 5000 | 23 | sample_id, drug_id, drug_name, cell_line_id, cell_line_name, response_value, response_metric, dataset_label |
| `data/frozen/topic_1_v3_baseline_20260505/topic_1_multiomics_response_vector_v3.csv` | 5000 | 3 | sample_id, response_value, response_metric |
| `data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_feature_matrix.csv` | 16611 | 1931 | sample_id, pathway_mean__Signal_Transduction, pathway_mean__Metabolism, pathway_mean__Immune_System, pathway_mean__Metabolism_of_proteins, pathway_mean__Disease, pathway_mean__Gene_expression_Transcription_, pathway_mean__Post_translational_protein_modification |
| `data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_sample_index.csv` | 16611 | 10 | sample_id, depmap_id, ccle_name, prism_compound_id, prism_compound_name, matched_gdsc_drug_id, matched_gdsc_drug_name, prism_response_metric |
| `data/frozen/topic_1_prism_external_validation_20260505/topic_1_prism_external_validation_response_vector.csv` | 16611 | 3 | sample_id, response_value, response_metric |

## Feature Groups

- `pathway_activity`: Reactome-derived pathway features.
- `mutation_hotspot_features` and `mutation_damaging_features`: mutation-derived features.
- `copy_number_features` and `global_signature_features`: CNV/global summary features.
- `drug_structure_morgan_fingerprint`: Morgan fingerprints where SMILES coverage was available.
- `drug_structure_missingness`: missingness indicator for drug structure coverage.
- `drug_identity_placeholder_control`: control/sensitivity features, not biological drug representations.
- `missing_modality_mask`: modality missingness indicators.

## Intended Use

- Internal baseline and proposed candidate model evaluation.
- PRISM candidate external validation with response-scale caveats.
- Sensitivity analyses, including no-drug-identity-placeholder ablation.
- Computational pathway attribution interpreted as hypothesis generation only.

## Restrictions and Limitations

- Original GDSC, DepMap/CCLE, PRISM, and Reactome data should be accessed from official sources.
- Redistribution of raw third-party data depends on the original providers' licenses and terms.
- PRISM LFC and GDSC LN_IC50 are different response scales; PRISM is used for ranking/correlation-oriented candidate validation.
- Low SMILES/Morgan coverage prevents strong drug-structure representation claims.
- No clinical reliability or mechanism validation claim is supported by these cleaned data structures.

## DATASET_VERSION_CARD.md

# Dataset Version Card

- dataset_name: topic_1_v3_multiomics_baseline
- version: topic_1_v3_baseline_20260505
- freeze_date: 2026-05-05T10:44:25.870137+00:00
- source data: GDSC response, DepMap expression, DepMap mutation matrices, DepMap global signatures, selected CNV features, Reactome pathway gene sets, DepMap/PortalCompounds drug metadata
- samples: 5000
- features: 1931
- response metric: LN_IC50
- feature groups:
  - copy_number_features: 100
  - drug_identity_placeholder_control: 613
  - drug_structure_missingness: 1
  - drug_structure_morgan_fingerprint: 256
  - global_signature_features: 6
  - missing_modality_mask: 4
  - mutation_damaging_features: 200
  - mutation_hotspot_features: 554
  - pathway_activity: 200
- missing modality handling: missing modality mask columns are included in sample index and separate mask file; missing omics features are zero-filled after mask creation
- drug structure coverage limitation: Morgan fingerprints are partial; low SMILES coverage prevents strong drug-structure representation claims
- known limitations: dry-run scale, incomplete drug structures, PRISM external validation not yet implemented, no final statistical claims
- intended use: internal baseline candidate experiments and proposed-model development preparation
- not intended use: final manuscript Results, clinical claims, causality/mechanism proof, strong drug-structure innovation claim


## PRISM_EXTERNAL_VALIDATION_DATASET_CARD.md

# PRISM External Validation Dataset Card

- freeze date: 20260505
- PRISM source: Repurposing Public 23Q2 local downloaded release
- response metric: LFC_COLLAPSED
- response direction: likely lower LFC means greater sensitivity / lower viability
- transform used: none for raw rank/correlation with predicted GDSC LN_IC50; no direct scale comparison
- number of ready pairs: 16797
- number of feature rows: 16611
- number of cell lines: 522
- number of drugs: 28
- feature columns including sample_id: 1931
- feature alignment with GDSC v3: column-aligned to frozen v3 feature matrix
- mapping rules: high-confidence DepMap ID and drug name/synonym mappings only
- excluded manual-review mappings: yes
- limitations: PRISM LFC and GDSC LN_IC50 are different scales; response direction still needs human confirmation; low SMILES/Morgan coverage limits drug-structure claims
- intended use: external validation candidate analysis
- not intended use: training, hyperparameter tuning, final claim without manual review
