# Anomaly Check

This report summarizes basic anomaly checks for [train.csv](../data/train.csv), [test.csv](../data/test.csv), and [sample_submission.csv](../data/sample_submission.csv).

## Overall Result

No critical data anomalies were found.

The dataset is structurally consistent:

- [train.csv](../data/train.csv) has 668,665 rows and 15 columns.
- [test.csv](../data/test.csv) has 286,571 rows and 14 columns.
- [sample_submission.csv](../data/sample_submission.csv) has 286,571 rows and 2 columns.
- There are no missing values in [train.csv](../data/train.csv) or [test.csv](../data/test.csv).
- There are no duplicate `id` values in train, test, or sample submission.
- Train and test IDs do not overlap.
- Test feature columns exactly match train feature columns after removing `Will_Buy_EV`.
- [sample_submission.csv](../data/sample_submission.csv) IDs exactly match [test.csv](../data/test.csv) IDs in the same order.

## Schema Checks

| Check | Result |
| --- | --- |
| Missing values in train | None |
| Missing values in test | None |
| Duplicate train IDs | 0 |
| Duplicate test IDs | 0 |
| Duplicate submission IDs | 0 |
| Train/test ID overlap | 0 |
| Train/test feature schema match | Pass |
| Submission IDs match test IDs | Pass |
| Unexpected test categories | None |

## Numeric Range Checks

| Column | Train Min | Train Max | Test Min | Test Max | Note |
| --- | ---: | ---: | ---: | ---: | --- |
| `Age` | 25 | 69 | 25 | 69 | Normal |
| `Annual_Income_USD` | 30,000 | 188,549 | 30,000 | 186,936 | High-income tail exists in both train and test |
| `Daily_Commute_km` | 5.0 | 98.7 | 5.0 | 103.9 | Test has a slightly higher max than train |
| `Number_of_Cars_Owned` | 1 | 4 | 1 | 4 | Normal discrete range |
| `Charging_Stations_Near_Home` | 0 | 14 | 0 | 14 | Normal |
| `Charging_Stations_Near_Work` | 0 | 19 | 0 | 19 | Normal |
| `Environmental_Concern_Level` | 1 | 5 | 1 | 5 | Expected scale |

## IQR Outlier Scan

Using train-set IQR bounds, most numeric columns show no concerning outliers. The following tail values were detected:

| Column | IQR Bounds | Train Count Outside Bounds | Test Count Outside Bounds | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `Annual_Income_USD` | 14,310.5 to 155,818.5 | 3,678 | 1,538 | Plausible high-income tail, not necessarily invalid |
| `Daily_Commute_km` | -28.1 to 92.7 | 41 | 14 | Very long commutes; likely rare but plausible |
| `Number_of_Cars_Owned` | -0.5 to 3.5 | 13,489 | 5,855 | Values of 4 are flagged only because the feature is discrete; 4 is within the documented observed range |

These should not be automatically removed. They appear to be valid tail observations rather than data errors.

## Categorical Checks

All categorical columns have the same category sets in train and test:

| Column | Categories |
| --- | --- |
| `Gender` | `Female`, `Male`, `Other` |
| `City_Type` | `Rural`, `Suburban`, `Urban` |
| `Current_Car_Type` | `Hatchback`, `SUV`, `Sedan`, `Truck` |
| `Home_Charging_Possible` | `No`, `Yes` |
| `Subsidy_Available` | `No`, `Yes` |
| `Range_Anxiety_Level` | `High`, `Low`, `Medium` |

Category proportions are also very similar between train and test. The largest observed train/test category proportion shift is about 0.17 percentage points for `Range_Anxiety_Level`.

## Submission Check

[sample_submission.csv](../data/sample_submission.csv) has one constant prediction value in `Will_Buy_EV`:

```text
0.17464500160768098
```

This is not an anomaly. It is a baseline/sample value and should be replaced by model predictions in final submissions.

Every method should still output the same final format:

```csv
id,Will_Buy_EV
668665,<prediction>
668666,<prediction>
668667,<prediction>
```

## Recommendations

- Keep all rows unless a modeling experiment proves that trimming tails improves validation.
- Preserve the exact [test.csv](../data/test.csv) / [sample_submission.csv](../data/sample_submission.csv) ID order for every submission.
- Treat `Will_Buy_EV = Yes` as the positive class when producing probability predictions.
- Do not treat the constant prediction in [sample_submission.csv](../data/sample_submission.csv) as a label; it is only the required output template.
