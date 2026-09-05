from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test.csv"
OUTPUT_PATH = DATA_DIR / "Will_Buy_EV.csv"
TARGET = "Will_Buy_EV"
POSITIVE_CLASS = "Yes"


def main():
    train = pd.read_csv(TRAIN_PATH, usecols=[TARGET])
    test = pd.read_csv(TEST_PATH, usecols=["id"])

    baseline_probability = train[TARGET].eq(POSITIVE_CLASS).mean()

    submission = test.copy()
    submission[TARGET] = baseline_probability
    submission.to_csv(OUTPUT_PATH, index=False)

    print(f"Baseline probability for {TARGET} = {POSITIVE_CLASS}: {baseline_probability}")
    print(f"Wrote {len(submission)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
