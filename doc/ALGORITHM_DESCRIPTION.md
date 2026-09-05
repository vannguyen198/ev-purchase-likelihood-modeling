# Algorithm Description

This project uses a feature-based logistic regression model to estimate the likelihood that each test-row `id` will have `Will_Buy_EV = Yes`.

The generated prediction file is:

```text
Will_Buy_EV.csv
```

It follows the required submission structure:

```csv
id,Will_Buy_EV
```

## Algorithm Used

The current algorithm is logistic regression with:

- Scaled numeric features
- One-hot encoded categorical features
- Binary target encoding where `Yes = 1` and `No = 0`
- Predicted probability output for the positive class, `Will_Buy_EV = Yes`

The implementation is in [make_likelihood_submission.py](../src/make_likelihood_submission.py).

## Modeling Pipeline

1. Read [train.csv](../data/train.csv) and [test.csv](../data/test.csv).
2. Convert the training target:

```text
Will_Buy_EV = Yes -> 1
Will_Buy_EV = No  -> 0
```

3. Split the training data into training and validation subsets.
4. Scale numeric features using `StandardScaler`.
5. Encode categorical features using `OneHotEncoder`.
6. Train a `LogisticRegression` classifier.
7. Validate the model using ROC AUC and log loss.
8. Refit the model on all training rows.
9. Predict probabilities for all rows in [test.csv](../data/test.csv).
10. Save the final predictions to [Will_Buy_EV.csv](../data/Will_Buy_EV.csv).

## Validation Performance

The logistic regression model produced:

| Metric | Value |
| --- | ---: |
| ROC AUC | 0.937953 |
| Log loss | 0.233580 |

ROC AUC measures how well the model ranks likely buyers above unlikely buyers. Log loss measures the quality of the predicted probabilities.

## Features Used

The model uses the following attributes from [train.csv](../data/train.csv) and [test.csv](../data/test.csv):

| Feature | Type | Preprocessing |
| --- | --- | --- |
| `Annual_Income_USD` | Numeric | Scaled |
| `Daily_Commute_km` | Numeric | Scaled |
| `Number_of_Cars_Owned` | Numeric | Scaled |
| `Charging_Stations_Near_Home` | Numeric | Scaled |
| `Charging_Stations_Near_Work` | Numeric | Scaled |
| `Environmental_Concern_Level` | Numeric | Scaled |
| `Gender` | Categorical | One-hot encoded |
| `City_Type` | Categorical | One-hot encoded |
| `Current_Car_Type` | Categorical | One-hot encoded |
| `Home_Charging_Possible` | Categorical | One-hot encoded |
| `Subsidy_Available` | Categorical | One-hot encoded |
| `Range_Anxiety_Level` | Categorical | One-hot encoded |

The `id` column is not used as a predictive feature. It is only preserved for the final output file.

## How Logistic Regression Uses Attributes

Logistic regression estimates a weighted score from the input features, then converts that score into a probability between 0 and 1.

Conceptually:

```text
score = intercept + weighted feature contributions
probability = sigmoid(score)
```

If a feature has a positive learned weight, higher values or matching categories increase the predicted likelihood of `Will_Buy_EV = Yes`. If a feature has a negative learned weight, higher values or matching categories decrease the predicted likelihood.

Because numeric features are scaled first, logistic regression can compare their effects more fairly. Because categorical features are one-hot encoded, each category can have its own learned contribution.

## Attribute Contributions

The exact contribution of each attribute is learned from the training data. In general, each feature contributes as follows:

| Attribute | How It Can Affect the Prediction |
| --- | --- |
| `Annual_Income_USD` | Income may affect affordability. Higher income can increase the likelihood if the model learns that EV buyers tend to have higher purchasing power. |
| `Daily_Commute_km` | Commute distance can affect EV usefulness and range concerns. Longer commutes may increase interest in fuel savings, but may also reduce interest if range anxiety is high. |
| `Number_of_Cars_Owned` | Existing vehicle ownership may indicate household vehicle needs and purchasing capacity. The model learns whether owning more cars is associated with higher or lower EV adoption. |
| `Charging_Stations_Near_Home` | More nearby home charging stations can make EV ownership more convenient, potentially increasing the predicted likelihood. |
| `Charging_Stations_Near_Work` | More charging options near work can reduce charging inconvenience, potentially increasing the predicted likelihood. |
| `Environmental_Concern_Level` | Higher environmental concern can increase the probability if environmentally concerned people are more likely to choose EVs. |
| `Gender` | The model checks whether observed purchase likelihood differs by gender category in the training data. This should be interpreted carefully because it may reflect correlations rather than direct causation. |
| `City_Type` | Urban, suburban, and rural settings can affect charging access, driving patterns, and EV practicality. |
| `Current_Car_Type` | Current vehicle type may reflect driving needs, lifestyle, or preferences that affect EV interest. |
| `Home_Charging_Possible` | Home charging is usually an important convenience factor and may strongly affect EV-buying likelihood. |
| `Subsidy_Available` | Subsidies reduce purchase cost, which can increase the likelihood of buying an EV. |
| `Range_Anxiety_Level` | Higher range anxiety can reduce EV-buying likelihood, while lower anxiety can increase it. |

## Why This Is Better Than the Sample Baseline

[sample_submission.csv](../data/sample_submission.csv) uses the same value for every ID. That is only a baseline/template and does not measure differences between individual rows.

The logistic regression model produces row-specific probabilities because it uses the actual feature values from [test.csv](../data/test.csv). This means two people can receive different likelihoods based on income, commute distance, charging access, environmental concern, and categorical attributes.

## Output Meaning

In [Will_Buy_EV.csv](../data/Will_Buy_EV.csv), each `Will_Buy_EV` value is:

```text
Predicted probability that the person will buy an EV
```

Example:

```csv
id,Will_Buy_EV
668665,0.004951200770027928
668666,0.0316869502410494
668667,0.005778976529079919
```

A higher value means a higher estimated likelihood of `Will_Buy_EV = Yes`.
