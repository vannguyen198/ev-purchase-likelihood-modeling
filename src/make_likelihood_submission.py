from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test.csv"
OUTPUT_PATH = DATA_DIR / "Will_Buy_EV.csv"
TARGET = "Will_Buy_EV"
POSITIVE_CLASS = "Yes"
RANDOM_STATE = 42

# Features requested for likelihood estimation.
NUMERIC_FEATURES = [
    "Annual_Income_USD",
    "Daily_Commute_km",
    "Number_of_Cars_Owned",
    "Charging_Stations_Near_Home",
    "Charging_Stations_Near_Work",
    "Environmental_Concern_Level",
]

CATEGORICAL_FEATURES = [
    "Gender",
    "City_Type",
    "Current_Car_Type",
    "Home_Charging_Possible",
    "Subsidy_Available",
    "Range_Anxiety_Level",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def build_model():
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(max_iter=1000, solver="lbfgs"),
            ),
        ]
    )


def main():
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)

    x = train[FEATURES]
    y = train[TARGET].eq(POSITIVE_CLASS).astype(int)

    x_train, x_valid, y_train, y_valid = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = build_model()
    model.fit(x_train, y_train)

    valid_probability = model.predict_proba(x_valid)[:, 1]
    print(f"Validation ROC AUC: {roc_auc_score(y_valid, valid_probability):.6f}")
    print(f"Validation log loss: {log_loss(y_valid, valid_probability):.6f}")

    # Refit on all training data before producing the final test likelihoods.
    model.fit(x, y)
    test_probability = model.predict_proba(test[FEATURES])[:, 1]

    submission = pd.DataFrame(
        {
            "id": test["id"],
            TARGET: test_probability,
        }
    )
    submission.to_csv(OUTPUT_PATH, index=False)

    print(f"Wrote {len(submission)} feature-based probabilities to {OUTPUT_PATH}")
    print(
        "Prediction range: "
        f"{submission[TARGET].min():.6f} to {submission[TARGET].max():.6f}"
    )


if __name__ == "__main__":
    main()
