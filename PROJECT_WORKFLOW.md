# Project Workflow: 30-Day Readmission Prediction

## 1) Business Problem Framing
- Objective: predict whether a diabetic inpatient will be readmitted within 30 days.
- Constraint: class imbalance requires recall-oriented evaluation.

## 2) Data Acquisition
- Source dataset loaded from `Dataset/raw/`.
- Mapping metadata used for categorical interpretation.

## 3) Data Audit
- Profiled schema, missingness, and categorical cardinality.
- Flagged leakage-prone identifiers and high-missingness variables.

## 4) Data Cleaning and Feature Engineering
- Standardized missing codes (`?`, `NaN`) into meaningful categories where appropriate.
- Removed non-predictive identifiers.
- Prepared cleaned dataset in `Dataset/cleaned/cleaned_data.csv`.

## 5) Exploratory Data Analysis (EDA)
- Measured class distribution and baseline risk.
- Identified strongest predictive signals:
  - prior inpatient utilization
  - discharge disposition
  - specialty and diagnosis patterns
  - medication/lab signals

## 6) Hypothesis Testing
- Tested statistically motivated clinical hypotheses from EDA.
- Used significance and effect-size interpretation for practical relevance.

## 7) Modeling
- Trained multiple classification models.
- Compared using Recall, PR-AUC, ROC-AUC, F1, and confusion matrix outputs.
- Selected top deployment candidates for risk screening use case.

## 8) Application Layer
- Implemented a Flask web app in `healthcare_app/`:
  - dashboard
  - audit/cleaning/EDA/hypothesis/model pages
  - risk prediction form and explanation

## 9) Portfolio Packaging
- Organized EDA visuals under `images/eda/`.
- Curated recruiter-facing findings under `images/main_findings/`.
- Created concise root `README.md` for quick project evaluation.
