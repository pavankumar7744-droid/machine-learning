# Master Prompt (v3) for Antigravity IDE: Purchase Prediction using XGBoost & LightGBM

Dataset: `online_shoppers_intention.csv` (UCI Online Shoppers Purchasing Intention). Put it in `data/raw/` first. Paste everything below the line into Antigravity.

---

## 0. Working rules

You are building a clean, modular academic ML project: **Purchase Prediction using XGBoost and LightGBM**. It is a binary classification problem on tabular data with a fair model comparison and explainability.

1. **Inspect before you assume.** Never invent columns, metrics, or conclusions. Every number in the README must come from a file the pipeline generated.
2. **Work in stages.** Run and verify each stage before starting the next.
3. **Use git.** `git init` at the start, add a `.gitignore`, and **commit after every stage**. Push to GitHub if I give a remote URL. (I lost this project once by deleting a folder.)
4. **Keep it proportionate.** It is a course project. Prefer a smaller pipeline I can fully explain in a viva.
5. **Report honestly.** Never redefine the target or add features just to raise a metric.
6. Use `pathlib`, no hard-coded OS paths.

---

## 1. The dataset (already inspected, so verify it)

- 12,330 rows × 18 columns, one row per browsing session. No missing values. **125 exact duplicate rows.**
- **Target: `Revenue`** (bool). `True` = the session ended in a purchase. Purchase rate is about 15.5% (about 15.6% after removing duplicates), so the data is imbalanced.
- Features:
  - Page counts and time spent: `Administrative, Administrative_Duration, Informational, Informational_Duration, ProductRelated, ProductRelated_Duration` (durations are in seconds)
  - Google Analytics metrics: `BounceRates, ExitRates, PageValues`
  - `SpecialDay` (closeness to a special day, 0 to 1)
  - Categorical or coded: `Month` (Feb, Mar, May, June, Jul, Aug, Sep, Oct, Nov, Dec; **January and April are absent**), `VisitorType` (Returning_Visitor, New_Visitor, Other), `Weekend` (bool), and the integer-coded `OperatingSystems, Browser, Region, TrafficType`

**Stage 1 must verify all of the above** and write any discrepancies to `results/metrics/data_audit.md`.

This dataset has **no cart additions, no previous-purchase history, and no product category**. Do not invent substitutes for them. The browsing-behavior features above are what exist.

---

## 2. Target

- `Revenue`: map `True → 1 (Purchase)` and `False → 0 (No purchase)`. Verify against the actual values before mapping.
- Print counts and percentages, and state the imbalance explicitly.

---

## 3. The `PageValues` issue (the most important section)

`PageValues` is the average value of the pages a visitor viewed **before reaching a transaction page**. It is computed using e-commerce transaction information, so it is partly derived from the outcome. In my checks:
- About 78% of sessions have `PageValues = 0`, and those sessions convert only about 4% of the time. Sessions with `PageValues > 0` convert about 56% of the time.
- Quick LightGBM/XGBoost results with the default setup: **ROC-AUC ≈ 0.93 with `PageValues`, ≈ 0.78–0.79 without it.** PR-AUC drops from about 0.75 to about 0.35.

So the model's headline quality depends heavily on one feature that may not be available in a real "predict before purchase" setting. Therefore:

- **Run every experiment in two variants:** `full` (all features) and `no_pagevalues`.
- Report both everywhere (metrics tables, ROC curves, SHAP).
- In the README, explain that `PageValues` is a strong but **potentially outcome-leaking** feature, that the `full` model shows the achievable upper bound, and that the `no_pagevalues` model is the more honest behavioral predictor. Do not present the `full` result alone as "the" result.
- Run an automated leakage check (`src/leakage_audit.py`) that reports single-feature cross-validated AUC on the training split for every feature, flags anything above a configurable threshold (default 0.80), and saves `results/metrics/leakage_audit.csv`. `BounceRates` and `ExitRates` should also be examined, since they are page-level analytics statistics.

---

## 4. Data cleaning

- Remove the 125 exact duplicates **before splitting**, and log the count in `results/metrics/cleaning_log.md`. Sessions have no ID, so identical rows may be separate sessions, but keeping them risks the same row landing in both train and test. Explain this decision and keep it configurable (`DROP_DUPLICATES=True`).
- Check ranges: counts and durations non-negative, `BounceRates`/`ExitRates` in [0, 0.2], `SpecialDay` in [0, 1]. Note that the heavily skewed durations and counts are real, so do not delete outliers without logging and justifying it.
- Log every cleaning action and the number of affected rows. Do not delete rows silently.

---

## 5. Splitting

- Stratified 80/20 on `Revenue`, `random_state=42`, both configurable.
- For the headline comparison use **repeated stratified cross-validation on the training set (e.g. 5 folds × 3 repeats)**, and keep a single untouched test set for the final confusion matrices, ROC curves, and SHAP plots.
- Validation data for early stopping and tuning comes only from the training set.
- **Optional robustness check:** a month-based split (e.g. train on Feb–Oct, test on Nov–Dec), reported separately. It tests generalization across time, and I expect lower scores because Nov/Dec behave differently.

---

## 6. Feature engineering (only what the data supports)

Document each engineered feature (name, formula, source columns, business reason, leakage check) in `results/metrics/feature_report.md`. Handle division by zero. Do not create arbitrary combinations.

Reasonable candidates:
- `total_pages = Administrative + Informational + ProductRelated`
- `total_duration = Administrative_Duration + Informational_Duration + ProductRelated_Duration`
- `avg_time_per_page = total_duration / total_pages` (guarded)
- `product_page_share = ProductRelated / total_pages`
- `product_time_share = ProductRelated_Duration / total_duration`
- `is_returning` and `is_new` from `VisitorType`
- `is_peak_season` (Nov/Dec), documented as a choice, not a discovery
- `has_pagevalue = PageValues > 0` (**only in the `full` variant**, and flagged in the leakage report)

Compare **baseline features vs engineered features** with the same CV protocol. If engineering does not help, say so and keep the simpler feature set.

---

## 7. Preprocessing

- One scikit-learn `ColumnTransformer` / `Pipeline`, fitted on **training data only**, saved with Joblib.
- Numeric: median imputation (no missing values now, but the pipeline should still be safe for new data) and optional scaling. Categorical: one-hot for `Month`, `VisitorType`, and treat the integer-coded `OperatingSystems, Browser, Region, TrafficType` as **categorical, not numeric**. Document how rare categories are handled.
- Feature scaling is included to satisfy the project report, but **state clearly that XGBoost and LightGBM do not require scaling**. Do not claim it improves them. Optionally include a small with/without-scaling check.
- Keep the transformed feature names for importance and SHAP plots.

---

## 8. Models and fair comparison

XGBoost (`binary:logistic`) and LightGBM (`binary`) with identical data, features, folds, and tuning budget.

- **Imbalance:** use `scale_pos_weight` for both. Compare weighted vs unweighted as a documented experiment.
- **Baseline** with fixed, configurable hyperparameters (`n_estimators, learning_rate, max_depth/num_leaves, subsample, colsample_bytree`). Then a **small** `RandomizedSearchCV` (≤ 30 iterations, stratified CV, training data only, **same budget and folds for both models**). Label Baseline vs Tuned clearly.
- Include a **dummy baseline** (always predict "no purchase") and a **logistic regression** baseline, so the reader can see what boosting adds.
- **Stability:** report mean ± std across CV folds and repeats. If XGBoost and LightGBM differ by less than the noise, say they are indistinguishable instead of declaring a winner. (In my quick check they were within about 0.005 AUC of each other.)
- Record training time (`time.perf_counter()` around `fit`), prediction time, and model file size. With about 10,000 rows the differences will be tiny, so report them honestly and do not claim a large efficiency advantage.

---

## 9. Evaluation

For both models and both variants (`full`, `no_pagevalues`):
- Accuracy, Precision, Recall, F1-Score, ROC-AUC (the five metrics required by the project report), plus **PR-AUC**. Accuracy alone is misleading (the dummy gets about 84%).
- Confusion matrix per model (labelled TN/FP/FN/TP), classification report, combined ROC curve and combined precision-recall curve with AUCs in the legend.
- **Decision threshold:** do not assume 0.5. Choose it on validation data (e.g. maximize F1, or meet a stated recall target), then apply it once to the test set. Include a threshold-vs-metric plot.
- Optional calibration curve, since the system outputs probabilities.
- Save to `results/metrics/` (`model_comparison.csv`, `evaluation_summary.json`) and `results/plots/`.

---

## 10. Explainability

- Gain-based feature importance (top 15) for both models, with readable feature names.
- **SHAP** (`shap.TreeExplainer`): global bar plot and beeswarm plot for both variants, plus local explanations for 3 sessions (a confident purchase, a confident non-purchase, a borderline one). Use a sample if needed and say so.
- Write interpretations **only** from the SHAP values. Expect `PageValues` to dominate the `full` model. Show what takes over once it is removed (likely `ExitRates`, `ProductRelated_Duration`, `Month`, `VisitorType`), but only state what the plots actually show.

---

## 11. Prediction module

`src/predict.py` loads the saved pipeline and model, accepts one session record (dict or CSV row), applies the same feature engineering and preprocessing, and prints:

~~~
Prediction: Likely to purchase   (or: Unlikely to purchase)
Purchase probability: 0.xxx
Non-purchase probability: 0.xxx
Model: XGBoost | LightGBM     Variant: full | no_pagevalues     Threshold: 0.xx
~~~

Give clear errors for missing columns or missing model files. Test loading the artifacts in a **fresh Python process** and reproducing predictions. Save library versions (`python, xgboost, lightgbm, scikit-learn, shap`) next to the models.

---

## 12. Project structure

~~~
purchase-prediction/
├── data/{raw,processed}/
├── notebooks/ (01_eda.ipynb, 02_results.ipynb)
├── src/ (__init__, data_loader, leakage_audit, feature_engineering,
│         preprocessing, train, evaluate, explainability, predict)
├── models/
├── results/{metrics,plots,shap}/
├── app/            # OPTIONAL, last
├── config.py  main.py  requirements.txt  README.md  .gitignore
~~~

Reusable logic lives in `src/`. Notebooks only call it. `main.py --stage eda|audit|features|train|evaluate|shap|all` so I can regenerate one result without retraining everything.

**Stack:** Python 3.10+, pandas, numpy, matplotlib, seaborn, scikit-learn, xgboost, lightgbm, **shap**, joblib. Pin versions in `requirements.txt`.

---

## 13. EDA

Shape, dtypes, missing values, duplicates, summary statistics, target distribution; numeric distributions (heavily right-skewed, so use log-scaled plots where helpful); categorical counts; correlation heatmap (expect `BounceRates` and `ExitRates` to be strongly correlated, and the three page-count/duration pairs to correlate with each other); purchase rate by `Month`, `VisitorType`, `Weekend`, `TrafficType`, and `SpecialDay`. In my check, purchase rate varies a lot by month (about 2% in Feb vs about 25% in Nov) and by visitor type (New about 25% vs Returning about 14%), but report whatever you actually find. Save plots to `results/plots/`.

---

## 14. Honest expectations

Based on my quick checks: **ROC-AUC ≈ 0.93 with `PageValues` and ≈ 0.78–0.80 without it**, with XGBoost and LightGBM close to each other. These ranges are consistent with the literature on this dataset. If you see AUC far above 0.95, investigate for a bug or leak before reporting. Do not change the protocol to chase a higher number.

---

## 15. Development order (verify and commit each)

1. Setup, git, load data, data audit
2. EDA and cleaning log
3. Leakage audit, then freeze the feature list and the two variants
4. Feature engineering and preprocessing pipeline
5. Splits, dummy and logistic baselines
6. Baseline XGBoost and LightGBM
7. Evaluation, threshold, repeated CV
8. Small tuning step (same budget for both)
9. Feature importance, then SHAP
10. Save models, `predict.py`, fresh-process test
11. README (real measured results only), requirements, cleanup
12. **Optional:** the month-based split, then a small Streamlit/Gradio app

## 16. README

Title, problem statement, dataset description (actual shape, columns, missing months, duplicates), target definition, the **`PageValues` discussion and both variants**, features, methodology diagram, splits, results tables generated from files, the XGBoost vs LightGBM comparison (performance, time, size, stability), SHAP findings, limitations (old 10-month data, no cart or purchase-history features, `PageValues` leakage risk, no January/April), how to run, and business applications **only as far as the results support**.

Also include a short note that the original project report mentions cart additions, previous purchases, and product category, and that this dataset does not contain them.

## 17. Hard "do not" list

No fabricated columns, features, metrics, or conclusions. No fitting preprocessing on the full dataset. No tuning or threshold choice on the test set. No evaluation on training predictions. No accuracy-only reporting. No presenting the `full` model alone as the result. No claim that scaling helps tree models. No silent row deletion. No skipped commits.

Start with Stage 1: set up the repo, load `data/raw/online_shoppers_intention.csv`, verify §1, and write the data audit. Stop and show me the audit before Stage 2.
