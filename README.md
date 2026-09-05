# EV Purchase Likelihood Modeling

This repository explores a binary classification task: predicting the probability that a person will buy an electric vehicle.

The final output format follows the competition-style submission structure:

```csv
id,Will_Buy_EV
```

## Dataset Source

This project uses data from a Kaggle Playground Series competition.

| Field | Description |
| --- | --- |
| Dataset | Playground Series Season 6, Episode 9 |
| Source | [Kaggle competition data page](https://www.kaggle.com/competitions/playground-series-s6e9/data) |
| Task | Binary classification for `Will_Buy_EV` |
| Use | Portfolio and educational modeling |

The required prediction format follows [data/sample_submission.csv](data/sample_submission.csv).

## Repository Structure

```text
.
|-- data/
|   |-- train.csv
|   |-- test.csv
|   |-- sample_submission.csv
|   |-- Will_Buy_EV.csv
|   `-- Will_Buy_EV_catboost.csv
|-- doc/
|   |-- DATA_DESCRIPTION.md
|   |-- ANOMALY_CHECK.md
|   |-- ALGORITHM_DESCRIPTION.md
|   `-- MODEL_OUTPUT_COMPARISON.md
|-- src/
|   |-- check_anomalies.py
|   |-- make_baseline_submission.py
|   |-- make_likelihood_submission.py
|   |-- make_catboost_submission.py
|   |-- s6e9-0-exact-twins-31-discrete-zero-shift.ipynb
|   `-- comparison_page/
|-- package.json
|-- requirements.txt
`-- README.md
```

## Models

Two feature-based models are included:

| Model | Script | Output |
| --- | --- | --- |
| Logistic regression | [src/make_likelihood_submission.py](src/make_likelihood_submission.py) | [data/Will_Buy_EV.csv](data/Will_Buy_EV.csv) |
| CatBoost | [src/make_catboost_submission.py](src/make_catboost_submission.py) | [data/Will_Buy_EV_catboost.csv](data/Will_Buy_EV_catboost.csv) |

## Dataset Structure Lessons

A Kaggle discussion notebook in [src/s6e9-0-exact-twins-31-discrete-zero-shift.ipynb](src/s6e9-0-exact-twins-31-discrete-zero-shift.ipynb) studies train/test shift and duplicate-like rows.

Key takeaways:

- Train and test show no measurable distribution shift under adversarial validation.
- About 30.668% of train rows have a twin across the 11 low-cardinality/discrete features.
- Those twins are not a useful leakage shortcut; a normal model beats twin-label lookup on the same rows.
- The dataset is partly "categories wearing numeric clothes," so tree models and target encoding are good future directions.

## Python Setup

```powershell
python -m pip install -r requirements.txt
```

Run anomaly checks:

```powershell
python src/check_anomalies.py
```

Generate logistic regression predictions:

```powershell
python src/make_likelihood_submission.py
```

Generate CatBoost predictions:

```powershell
python src/make_catboost_submission.py
```

## Comparison Page

The model comparison page is available at:

[src/comparison_page/index.html](src/comparison_page/index.html)

To rebuild the TypeScript:

```powershell
npm.cmd install
npm.cmd run build:comparison
```

## Documentation

- [Data description](doc/DATA_DESCRIPTION.md)
- [Anomaly check](doc/ANOMALY_CHECK.md)
- [Algorithm description](doc/ALGORITHM_DESCRIPTION.md)
- [Model output comparison](doc/MODEL_OUTPUT_COMPARISON.md)
- [Discussion notebook insights](doc/DISCUSSION_NOTEBOOK_INSIGHTS.md)
