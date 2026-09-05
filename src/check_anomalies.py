import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

train = pd.read_csv(DATA_DIR / "train.csv")
test = pd.read_csv(DATA_DIR / "test.csv")
submission = pd.read_csv(DATA_DIR / "sample_submission.csv")

report = {}
report["shapes"] = {
    "train": train.shape,
    "test": test.shape,
    "sample_submission": submission.shape,
}
report["missing_train"] = train.isna().sum()[train.isna().sum() > 0].to_dict()
report["missing_test"] = test.isna().sum()[test.isna().sum() > 0].to_dict()
report["duplicate_ids"] = {
    "train": int(train["id"].duplicated().sum()),
    "test": int(test["id"].duplicated().sum()),
    "sample_submission": int(submission["id"].duplicated().sum()),
}
report["id_overlap_train_test"] = int(len(set(train["id"]).intersection(set(test["id"]))))
report["schema_match_features"] = list(train.drop(columns=["Will_Buy_EV"]).columns) == list(
    test.columns
)
report["submission_id_matches_test"] = submission["id"].equals(test["id"])

num_cols = train.select_dtypes(include="number").columns.drop("id")
report["numeric_ranges"] = {
    c: {
        "train_min": float(train[c].min()),
        "train_max": float(train[c].max()),
        "test_min": float(test[c].min()),
        "test_max": float(test[c].max()),
    }
    for c in num_cols
    if c in test.columns
}

cat_cols = train.select_dtypes(include="object").columns.drop("Will_Buy_EV")
category_mismatches = {}
for col in cat_cols:
    train_values = set(train[col].unique())
    test_values = set(test[col].unique())
    if train_values != test_values:
        category_mismatches[col] = {
            "train_only": sorted(train_values - test_values),
            "test_only": sorted(test_values - train_values),
        }
report["category_mismatches"] = category_mismatches

report["constant_columns"] = {
    "train": [c for c in train.columns if train[c].nunique(dropna=False) == 1],
    "test": [c for c in test.columns if test[c].nunique(dropna=False) == 1],
    "sample_submission": [
        c for c in submission.columns if submission[c].nunique(dropna=False) == 1
    ],
}

iqr_outliers = {}
for col in num_cols:
    q1 = train[col].quantile(0.25)
    q3 = train[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    iqr_outliers[col] = {
        "bounds": [float(lower), float(upper)],
        "train_count": int(((train[col] < lower) | (train[col] > upper)).sum()),
        "test_count": int(((test[col] < lower) | (test[col] > upper)).sum()),
    }
report["iqr_outliers"] = iqr_outliers

report["numeric_mean_shift"] = {
    col: {
        "train_mean": float(train[col].mean()),
        "test_mean": float(test[col].mean()),
        "mean_diff": float(test[col].mean() - train[col].mean()),
    }
    for col in num_cols
}

category_shift = {}
for col in cat_cols:
    train_prop = train[col].value_counts(normalize=True)
    test_prop = test[col].value_counts(normalize=True)
    values = sorted(set(train_prop.index) | set(test_prop.index))
    category_shift[col] = max(
        abs(float(test_prop.get(value, 0) - train_prop.get(value, 0))) for value in values
    )
report["max_category_prop_shift"] = category_shift

print(json.dumps(report, indent=2))
