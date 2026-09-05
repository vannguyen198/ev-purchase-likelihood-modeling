# Data Description

This project contains three CSV files for a binary classification task: predict whether a person will buy an electric vehicle.

## Files

| File | Rows | Columns | Purpose |
| --- | ---: | ---: | --- |
| [train.csv](../data/train.csv) | 668,665 | 15 | Training data with features and the target column `Will_Buy_EV`. |
| [test.csv](../data/test.csv) | 286,571 | 14 | Test data with the same feature columns as [train.csv](../data/train.csv), excluding the target. |
| [sample_submission.csv](../data/sample_submission.csv) | 286,571 | 2 | Required final output format for submissions and for the final output of every modeling method. |

Row counts exclude the header row.

## Prediction Target

`Will_Buy_EV` is the target variable.

In [train.csv](../data/train.csv), `Will_Buy_EV` is categorical:

| Value | Count |
| --- | ---: |
| `No` | 551,886 |
| `Yes` | 116,779 |

In [sample_submission.csv](../data/sample_submission.csv), `Will_Buy_EV` is numeric. Each row should contain the prediction for the matching `id` in [test.csv](../data/test.csv). For classification methods that produce probabilities, this column should typically contain the predicted probability for the positive class, `Yes`.

Important: [sample_submission.csv](../data/sample_submission.csv) is the final output format of every possible method. No matter which model, ensemble, rule-based method, or experiment is used, the final saved prediction file should have exactly these columns:

```text
id,Will_Buy_EV
```

## Column Schema

| Column | Present In | Type | Description |
| --- | --- | --- | --- |
| `id` | Train, Test, Submission | Integer | Unique row identifier. Test IDs must be preserved in the final submission. |
| `Age` | Train, Test | Integer | Person's age in years. |
| `Annual_Income_USD` | Train, Test | Float | Annual income in USD. |
| `Daily_Commute_km` | Train, Test | Float | Daily commute distance in kilometers. |
| `Number_of_Cars_Owned` | Train, Test | Integer | Number of cars currently owned. |
| `Charging_Stations_Near_Home` | Train, Test | Integer | Count of charging stations near home. |
| `Charging_Stations_Near_Work` | Train, Test | Integer | Count of charging stations near work. |
| `Environmental_Concern_Level` | Train, Test | Float | Environmental concern score from 1 to 5. |
| `Gender` | Train, Test | Categorical | One of `Female`, `Male`, `Other`. |
| `City_Type` | Train, Test | Categorical | One of `Rural`, `Suburban`, `Urban`. |
| `Current_Car_Type` | Train, Test | Categorical | One of `Hatchback`, `SUV`, `Sedan`, `Truck`. |
| `Home_Charging_Possible` | Train, Test | Categorical | Whether home charging is possible: `Yes` or `No`. |
| `Subsidy_Available` | Train, Test | Categorical | Whether an EV subsidy is available: `Yes` or `No`. |
| `Range_Anxiety_Level` | Train, Test | Categorical | One of `High`, `Low`, `Medium`. |
| `Will_Buy_EV` | Train, Submission | Target / Prediction | Training label in [train.csv](../data/train.csv); prediction value in [sample_submission.csv](../data/sample_submission.csv). |

## Numeric Feature Ranges

The following ranges are from [train.csv](../data/train.csv).

| Column | Minimum | Maximum | Mean |
| --- | ---: | ---: | ---: |
| `Age` | 25 | 69 | 47.04 |
| `Annual_Income_USD` | 30,000.00 | 188,549.00 | 84,769.27 |
| `Daily_Commute_km` | 5.00 | 98.70 | 32.16 |
| `Number_of_Cars_Owned` | 1 | 4 | 1.71 |
| `Charging_Stations_Near_Home` | 0 | 14 | 4.96 |
| `Charging_Stations_Near_Work` | 0 | 19 | 7.18 |
| `Environmental_Concern_Level` | 1.00 | 5.00 | 2.94 |

## Missing Values

There are no missing values in [train.csv](../data/train.csv) or [test.csv](../data/test.csv) for any column.

## Submission Requirements

Every final prediction file should:

1. Use the same `id` values and row order as [test.csv](../data/test.csv) / [sample_submission.csv](../data/sample_submission.csv).
2. Contain only two columns: `id` and `Will_Buy_EV`.
3. Store predictions in `Will_Buy_EV`.
4. Be saved as a CSV file that follows the [sample_submission.csv](../data/sample_submission.csv) structure.

Example:

```csv
id,Will_Buy_EV
668665,0.17464500160768098
668666,0.17464500160768098
668667,0.17464500160768098
```
