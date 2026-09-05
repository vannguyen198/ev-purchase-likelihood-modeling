from pathlib import Path

import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test.csv"
OUTPUT_PATH = DATA_DIR / "Will_Buy_EV_catboost.csv"
TARGET = "Will_Buy_EV"
POSITIVE_CLASS = "Yes"
RANDOM_STATE = 42

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


def build_model(use_overfitting_detector=True):
    params = {
        "iterations": 400,
        "learning_rate": 0.06,
        "depth": 5,
        "loss_function": "Logloss",
        "eval_metric": "AUC",
        "random_seed": RANDOM_STATE,
        "auto_class_weights": "Balanced",
        "allow_writing_files": False,
        "thread_count": -1,
        "verbose": 50,
    }
    if use_overfitting_detector:
        params.update(
            {
                "od_type": "Iter",
                "od_wait": 50,
            }
        )
    return CatBoostClassifier(**params)


def main():
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)
    print(f"Loaded train={train.shape}, test={test.shape}")

    x = train[FEATURES]
    y = train[TARGET].eq(POSITIVE_CLASS).astype(int)

    x_train, x_valid, y_train, y_valid = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    train_pool = Pool(
        x_train,
        y_train,
        cat_features=CATEGORICAL_FEATURES,
    )
    valid_pool = Pool(
        x_valid,
        y_valid,
        cat_features=CATEGORICAL_FEATURES,
    )

    model = build_model()
    print("Training validation CatBoost model...")
    model.fit(train_pool, eval_set=valid_pool, use_best_model=True)

    valid_probability = model.predict_proba(valid_pool)[:, 1]
    print(f"Validation ROC AUC: {roc_auc_score(y_valid, valid_probability):.6f}")
    print(f"Validation log loss: {log_loss(y_valid, valid_probability):.6f}")

    # Refit on all training data before producing final test probabilities.
    final_pool = Pool(x, y, cat_features=CATEGORICAL_FEATURES)
    test_pool = Pool(test[FEATURES], cat_features=CATEGORICAL_FEATURES)

    final_model = build_model(use_overfitting_detector=False)
    best_iteration = model.get_best_iteration()
    if best_iteration is not None and best_iteration > 0:
        final_model.set_params(iterations=best_iteration + 1)
    final_model.set_params(verbose=100)
    print("Training final CatBoost model on all rows...")
    final_model.fit(final_pool)

    test_probability = final_model.predict_proba(test_pool)[:, 1]

    submission = pd.DataFrame(
        {
            "id": test["id"],
            TARGET: test_probability,
        }
    )
    submission.to_csv(OUTPUT_PATH, index=False)

    print(f"Wrote {len(submission)} CatBoost probabilities to {OUTPUT_PATH}")
    print(
        "Prediction range: "
        f"{submission[TARGET].min():.6f} to {submission[TARGET].max():.6f}"
    )


if __name__ == "__main__":
    main()
