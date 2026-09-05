# Model Output Comparison

This file compares the two feature-based prediction files:

| File | Model | Output |
| --- | --- | --- |
| [Will_Buy_EV.csv](../data/Will_Buy_EV.csv) | Logistic regression | Probability of `Will_Buy_EV = Yes` |
| [Will_Buy_EV_catboost.csv](../data/Will_Buy_EV_catboost.csv) | CatBoost classifier | Probability of `Will_Buy_EV = Yes` |

Both files are based on the same training data, [train.csv](../data/train.csv), and predict on the same rows from [test.csv](../data/test.csv).

## Format Check

| Check | Result |
| --- | --- |
| Same number of rows | Pass |
| Same columns | Pass |
| Same ID order | Pass |
| IDs match [test.csv](../data/test.csv) | Pass |

Both files contain:

```csv
id,Will_Buy_EV
```

with 286,571 prediction rows.

## Prediction Distribution

| Statistic | Logistic Regression | CatBoost |
| --- | ---: | ---: |
| Mean | 0.174844 | 0.294772 |
| Standard deviation | 0.266894 | 0.354642 |
| Minimum | 0.000001 | 0.000003 |
| 25th percentile | 0.002407 | 0.010853 |
| Median | 0.024020 | 0.087422 |
| 75th percentile | 0.255027 | 0.642506 |
| Maximum | 0.971852 | 0.987875 |
| Unique prediction values | 285,908 | 284,173 |

CatBoost produces higher and more spread-out probabilities than logistic regression. Logistic regression stays closer to the original training target rate, while CatBoost separates likely and unlikely buyers more aggressively.

## Difference Summary

Difference is calculated as:

```text
CatBoost probability - Logistic regression probability
```

| Statistic | Difference |
| --- | ---: |
| Mean difference | 0.119927 |
| Standard deviation | 0.136046 |
| Minimum difference | -0.318845 |
| Median difference | 0.058323 |
| Maximum difference | 0.627250 |
| Mean absolute difference | 0.119990 |

CatBoost gives a higher probability than logistic regression for 283,069 rows. Logistic regression gives a higher probability for 3,502 rows.

## Agreement

| Agreement Check | Value |
| --- | ---: |
| Pearson correlation | 0.942903 |
| Spearman rank correlation | 0.991285 |
| Same side of 0.5 threshold | 86.51% |
| Logistic predictions >= 0.5 | 45,773 rows |
| CatBoost predictions >= 0.5 | 84,415 rows |

The very high Spearman correlation means the two models rank rows similarly. However, CatBoost often assigns larger probabilities, so it classifies many more rows above the 0.5 threshold.

## Biggest Differences

Rows where CatBoost predicts much higher than logistic regression:

| id | Logistic | CatBoost | Difference | Income | Commute | Cars | Home Stations | Work Stations | Concern | Gender | City | Car Type | Home Charging | Subsidy | Range Anxiety |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 702729 | 0.118010 | 0.745260 | 0.627250 | 68,530 | 15.0 | 1 | 1 | 3 | 3 | Female | Rural | SUV | Yes | Yes | Low |
| 695839 | 0.119238 | 0.710772 | 0.591534 | 68,480 | 14.3 | 3 | 0 | 0 | 3 | Female | Rural | Hatchback | Yes | Yes | Low |
| 859836 | 0.260082 | 0.845603 | 0.585522 | 110,152 | 12.7 | 1 | 1 | 8 | 3 | Male | Suburban | Sedan | Yes | Yes | Low |
| 782353 | 0.261878 | 0.845134 | 0.583257 | 109,418 | 15.0 | 2 | 1 | 5 | 3 | Male | Suburban | SUV | Yes | Yes | Low |
| 696196 | 0.115939 | 0.690771 | 0.574832 | 67,864 | 12.5 | 2 | 2 | 3 | 3 | Female | Rural | Hatchback | Yes | Yes | Low |

Rows where logistic regression predicts higher than CatBoost:

| id | Logistic | CatBoost | Difference | Income | Commute | Cars | Home Stations | Work Stations | Concern | Gender | City | Car Type | Home Charging | Subsidy | Range Anxiety |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 699784 | 0.563510 | 0.244665 | -0.318845 | 63,750 | 67.5 | 1 | 1 | 2 | 5 | Female | Rural | SUV | Yes | Yes | Low |
| 947946 | 0.561905 | 0.270939 | -0.290966 | 63,818 | 69.1 | 2 | 2 | 2 | 5 | Male | Rural | Sedan | Yes | Yes | Low |
| 808015 | 0.551633 | 0.289067 | -0.262566 | 63,794 | 67.3 | 2 | 5 | 7 | 5 | Male | Suburban | SUV | Yes | Yes | Low |
| 676525 | 0.555213 | 0.318854 | -0.236359 | 62,967 | 67.7 | 2 | 0 | 3 | 5 | Male | Rural | Sedan | Yes | Yes | Low |
| 706065 | 0.544786 | 0.327014 | -0.217771 | 63,919 | 67.2 | 1 | 5 | 9 | 5 | Male | Suburban | SUV | Yes | Yes | Low |

## Why They Differ On The Same Dataset

The two models use the same train/test files, but they learn different relationships.

Logistic regression learns a mostly linear relationship:

```text
probability = sigmoid(intercept + weighted feature values)
```

This means each feature contributes in a relatively smooth, additive way. For example, higher environmental concern or lower range anxiety can push the probability up, but logistic regression does not naturally capture complex feature combinations unless they are manually engineered.

CatBoost is a gradient-boosted decision tree model. It can learn:

- Nonlinear thresholds
- Interactions between features
- Different effects for the same feature under different conditions
- Native categorical splits

For example, CatBoost can learn that a row with `Subsidy_Available = Yes`, `Home_Charging_Possible = Yes`, `Range_Anxiety_Level = Low`, and a short commute is much more likely than those features would suggest individually. Logistic regression tends to add those effects more simply.

## Observed Pattern

In the biggest CatBoost-higher cases, the rows often include:

- Low `Range_Anxiety_Level`
- `Subsidy_Available = Yes`
- `Home_Charging_Possible = Yes`
- Shorter daily commute
- Moderate environmental concern

CatBoost appears to reward these combinations strongly.

In the biggest logistic-higher cases, the rows often include:

- Very high `Environmental_Concern_Level`
- Long daily commute around 67 to 69 km
- `Subsidy_Available = Yes`
- `Home_Charging_Possible = Yes`
- Low range anxiety

Logistic regression appears to give more direct additive credit to environmental concern and commute distance, while CatBoost moderates those rows based on learned tree patterns.

## Which Output Should Be Preferred

Based on validation ROC AUC:

| Model | Validation ROC AUC |
| --- | ---: |
| Logistic regression | 0.937953 |
| CatBoost | 0.940719 |

CatBoost has the stronger validation ranking performance, so [Will_Buy_EV_catboost.csv](../data/Will_Buy_EV_catboost.csv) is the better candidate if choosing between these two outputs.

However, CatBoost's log loss is worse in this run:

| Model | Validation Log Loss |
| --- | ---: |
| Logistic regression | 0.233580 |
| CatBoost | 0.320222 |

This means CatBoost ranks rows better, but its probabilities may be less calibrated. If the competition metric is ROC AUC, prefer CatBoost. If the metric is log loss, prefer logistic regression or calibrate CatBoost probabilities before submission.

## Effectiveness Comparison

| Comparison Area | Logistic Regression | CatBoost | More Effective | Why |
| --- | --- | --- | --- | --- |
| Ranking likely buyers above unlikely buyers | ROC AUC = 0.937953 | ROC AUC = 0.940719 | CatBoost | CatBoost has the higher ROC AUC, meaning it separates positive and negative cases slightly better. |
| Probability calibration | Log loss = 0.233580 | Log loss = 0.320222 | Logistic regression | Logistic regression has lower log loss, meaning its probability values are more reliable in this validation run. |
| Capturing nonlinear patterns | Limited | Strong | CatBoost | CatBoost can learn thresholds and curved relationships, such as different effects for short, medium, and long commutes. |
| Capturing feature interactions | Limited unless manually engineered | Strong | CatBoost | CatBoost can learn combinations such as `Subsidy_Available = Yes` plus `Home_Charging_Possible = Yes` plus `Range_Anxiety_Level = Low`. |
| Handling categorical attributes | Requires one-hot encoding | Native categorical handling | CatBoost | CatBoost can use categorical splits directly and may capture category behavior more naturally. |
| Simplicity and explainability | Strong | Moderate | Logistic regression | Logistic regression coefficients are easier to inspect and explain as positive or negative contributions. |
| Stability as a baseline | Strong | Moderate | Logistic regression | Logistic regression is less complex and less likely to overfit when feature relationships are simple. |
| Prediction confidence spread | More conservative | More aggressive | Depends on metric | CatBoost produces wider probabilities, which helps ranking but can hurt log loss if probabilities are overconfident. |
| Best current submission for ROC AUC metric | Good | Better | CatBoost | CatBoost scored higher on validation ROC AUC. |
| Best current submission for log loss metric | Better | Worse | Logistic regression | Logistic regression scored lower on validation log loss. |

Overall:

| Goal | Recommended Output |
| --- | --- |
| Maximize ranking quality / ROC AUC | [Will_Buy_EV_catboost.csv](../data/Will_Buy_EV_catboost.csv) |
| Maximize probability accuracy / log loss | [Will_Buy_EV.csv](../data/Will_Buy_EV.csv) |
| Need a simple, explainable model | Logistic regression |
| Need a stronger tabular model that captures interactions | CatBoost |

CatBoost is more effective when the goal is to rank IDs by EV-buying likelihood because it learns nonlinear rules and interactions from the same attributes. Logistic regression is more effective when the goal is well-calibrated probability output because its predictions are less aggressive and produced lower validation log loss here.
