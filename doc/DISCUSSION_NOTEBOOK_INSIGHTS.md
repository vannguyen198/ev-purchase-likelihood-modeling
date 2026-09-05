# Discussion Notebook Insights

This note summarizes useful documentation improvements found in the discussion notebook:

[s6e9-0-exact-twins-31-discrete-zero-shift.ipynb](../src/s6e9-0-exact-twins-31-discrete-zero-shift.ipynb)

The notebook is reference material from a Kaggle discussion page. It is useful because it studies the dataset structure, not just model scores.

## Main Takeaways

| Finding | Notebook Result | Why It Matters |
| --- | ---: | --- |
| Train/test shift | Adversarial AUC `0.499648` | Train and test appear interchangeable, so normal cross-validation on train is a reasonable estimate of test behavior. |
| Permutation null | Mean AUC `0.499642`, SD `0.002304` | The train/test adversarial result is essentially identical to shuffled labels, so there is no measurable distribution shift. |
| Exact duplicate rows | `0.000%` of train | There are no exact twins across all 13 features. |
| Discrete-feature twin rows | `30.668%` of train | Many rows share the same values across low-cardinality features, but this is not automatically a leak. |
| Test rows with train discrete twin | `30.629%` of test | The same discrete-key repetition appears in test, reinforcing that this is dataset structure rather than a direct label leak. |
| Twin lookup AUC | `0.771042` on discrete-twin rows | Looking up labels from matching rows performs much worse than a normal model. |
| Model AUC on same twin rows | `0.933026` | The model already captures the useful signal from those repeated discrete patterns. |
| 50/50 twin lookup blend | `0.909027` | Blending in the twin lookup hurts instead of helping. |
| Plain LightGBM baseline | AUC `0.941766` | A straightforward tree model is a strong benchmark for this dataset. |
| Nested blend gain | `+0.000221` AUC | The gain is only about `0.14` public leaderboard standard errors, likely too small to trust as a real leaderboard improvement. |

## What This Improves In The Project Docs

The existing docs should not only describe the data and the two current models. They should also explain which tempting ideas are probably not worth spending time on.

Good additions:

| Documentation Area | Improvement |
| --- | --- |
| Data description | Mention that most columns are low-cardinality or discrete-like, even when stored as numeric. |
| Anomaly check | Add that discrete twins are common but not evidence of leakage. |
| Algorithm notes | Add that target encoding or tree models may suit this dataset because many features behave like categories. |
| Model comparison | Explain why CatBoost and other tree models can benefit from repeated discrete patterns more naturally than pure linear models. |
| Future work | Suggest target encoding, LightGBM, calibrated CatBoost, and honest OOF validation before ensembling. |

## Discrete Features

The notebook treats features with at most 50 distinct values as discrete. Under that rule, 11 features are discrete and 2 are continuous.

| Feature | Distinct Values | Interpretation |
| --- | ---: | --- |
| `Home_Charging_Possible` | 2 | Binary categorical |
| `Subsidy_Available` | 2 | Binary categorical |
| `Gender` | 3 | Categorical |
| `City_Type` | 3 | Categorical |
| `Range_Anxiety_Level` | 3 | Categorical |
| `Number_of_Cars_Owned` | 4 | Discrete numeric |
| `Current_Car_Type` | 4 | Categorical |
| `Environmental_Concern_Level` | 5 | Ordinal / discrete numeric |
| `Charging_Stations_Near_Home` | 15 | Count feature |
| `Charging_Stations_Near_Work` | 20 | Count feature |
| `Age` | 45 | Discrete numeric |
| `Daily_Commute_km` | 805 | Continuous-like numeric |
| `Annual_Income_USD` | 13,214 | Continuous-like numeric |

This supports an important modeling idea: the dataset is partly "categories wearing numeric clothes." Numeric scaling helps logistic regression, but tree models and target encoding may capture the discrete structure better.

## No Train/Test Shift

The notebook performs adversarial validation by training a model to distinguish train rows from test rows.

Result:

```text
train vs test observed AUC: 0.499648
permutation null mean:      0.499642
permutation null SD:        0.002304
```

Interpretation:

```text
No measurable train/test distribution shift.
```

This means the validation split from [train.csv](../data/train.csv) is likely meaningful for estimating performance on [test.csv](../data/test.csv).

## Discrete Twins Are Not A Leak

The notebook finds:

```text
Rows in a discrete-feature twin group: 205,065
Percent of train: 30.668%
Twin groups: 82,534
Mean twin group size: 2.48
Twin groups label-pure: 77.280%
```

This is tempting because repeated rows can look like leakage. But the notebook tests that directly using a leave-one-out twin lookup.

| Method On Twin Rows | AUC |
| --- | ---: |
| Twin-label lookup | 0.771042 |
| Plain model | 0.933026 |
| 50/50 rank blend | 0.909027 |

The lookup is much weaker than a model, and blending it hurts. So the repeated discrete patterns are real, but they should be modeled normally rather than exploited as a lookup leak.

## Modeling Implications

| Idea | Recommendation | Reason |
| --- | --- | --- |
| Remove duplicate-like rows | Do not do this by default | The twins are valid structure, not corrupted data. |
| Use `id` as a feature | Avoid | IDs are sequential row identifiers, not meaningful buyer attributes. |
| Use train cross-validation | Yes | No measurable train/test shift was found. |
| Try LightGBM | Yes | The notebook's plain LightGBM baseline reached AUC `0.941766`. |
| Try target encoding | Yes | The notebook says target-encoding numeric, categorical, and digit-like columns as categories was a strong feature gain in related discussion work. |
| Blind ensembling | Be careful | The notebook's nested blend gain was only `+0.000221`, likely below public leaderboard noise. |
| Calibrate CatBoost | Worth trying | Current project CatBoost ranks well but has worse log loss than logistic regression. |

## Recommended Future Documentation

Add a short "Dataset Structure Lessons" section to the README:

```md
## Dataset Structure Lessons

Discussion analysis suggests that train and test have no measurable distribution shift.
About 30.668% of training rows have a twin across the 11 low-cardinality/discrete features,
but this does not behave like a leakage lever: a leave-one-out twin lookup performs far
worse than a normal model on the same rows.

This supports using cross-validation, tree models, and possibly target encoding, while
avoiding duplicate-row lookup tricks.
```

## Source Note

The notebook itself notes that some referenced Kaggle links should be replaced with exact notebook URLs before relying on them as formal citations. For GitHub documentation, keep this page as a technical summary unless the exact discussion/notebook URL is added.
