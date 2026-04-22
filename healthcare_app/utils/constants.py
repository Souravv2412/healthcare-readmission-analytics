# utils/constants.py
# All precomputed data from the notebook pipeline  -  no runtime recomputation needed.

PROJECT_TITLE = "30-Day Readmission Risk"
PROJECT_SUBTITLE = "Diabetes 130-US Hospitals · Predictive Analytics"
DATASET_NAME = "Diabetes 130-US Hospitals Dataset"

# ─── Dataset Overview ─────────────────────────────────────────────────────────
DATASET_STATS = {
    "total_encounters": 101_766,
    "total_columns_raw": 50,
    "total_columns_cleaned": 47,
    "unique_patients": 71_518,
    "positive_class_count": 11_357,
    "negative_class_count": 90_409,
    "positive_class_pct": 11.2,
    "negative_class_pct": 88.8,
    "imbalance_ratio": "8:1",
    "mean_age": 66.0,
    "mean_time_in_hospital": 4.4,
    "mean_prior_inpatient": 0.64,
    "insulin_dependent_pct": 53.4,
    "on_diabetes_med_pct": 77.0,
    "emergency_admissions_pct": 53.1,
    "discharged_to_home_pct": 59.2,
    "year_range": "1999–2008",
    "hospitals": 130,
    "country": "USA",
}

# ─── Data Audit Findings ──────────────────────────────────────────────────────
AUDIT_COLUMN_GROUPS = [
    {
        "group": "Identifiers",
        "columns": ["encounter_id", "patient_nbr"],
        "description": "Row and patient keys  -  not predictive features",
        "action": "Dropped (data leakage risk)",
        "badge": "dropped",
    },
    {
        "group": "Demographics",
        "columns": ["race", "gender", "age", "weight"],
        "description": "Patient characteristics",
        "action": "Cleaned & transformed",
        "badge": "cleaned",
    },
    {
        "group": "Admission / Discharge",
        "columns": [
            "admission_type_id",
            "discharge_disposition_id",
            "admission_source_id",
            "time_in_hospital",
        ],
        "description": "Hospital encounter metadata",
        "action": "ID codes mapped to labels",
        "badge": "mapped",
    },
    {
        "group": "Clinical",
        "columns": [
            "num_lab_procedures",
            "num_procedures",
            "num_medications",
            "number_outpatient",
            "number_emergency",
            "number_inpatient",
            "diag_1–3",
            "number_diagnoses",
            "max_glu_serum",
            "A1Cresult",
        ],
        "description": "Lab results, diagnoses, service utilisation",
        "action": "Missing values handled",
        "badge": "cleaned",
    },
    {
        "group": "Medications",
        "columns": ["23 drug columns", "change", "diabetesMed"],
        "description": "Individual diabetes medication dosage changes",
        "action": "Kept as categorical features",
        "badge": "kept",
    },
    {
        "group": "Target",
        "columns": ["readmitted"],
        "description": "Outcome variable: <30, >30, NO",
        "action": "Binarised → readmitted_binary",
        "badge": "target",
    },
]

MISSING_VALUES = [
    {"column": "weight", "count": 98_569, "pct": 96.9, "type": "? placeholder", "action": "Dropped (97% missing)"},
    {"column": "max_glu_serum", "count": 96_420, "pct": 94.7, "type": "Genuine NaN", "action": "Filled → 'Unknown'"},
    {"column": "A1Cresult", "count": 84_748, "pct": 83.3, "type": "Genuine NaN", "action": "Filled → 'Unknown'"},
    {"column": "medical_specialty", "count": 49_949, "pct": 49.1, "type": "? placeholder", "action": "Replaced → 'Unknown'"},
    {"column": "payer_code", "count": 40_256, "pct": 39.6, "type": "? placeholder", "action": "Replaced → 'Unknown'"},
    {"column": "race", "count": 2_273, "pct": 2.2, "type": "? placeholder", "action": "Replaced → 'Unknown'"},
    {"column": "diag_3", "count": 1_423, "pct": 1.4, "type": "? placeholder", "action": "Replaced → 'Unknown'"},
    {"column": "diag_2", "count": 358, "pct": 0.4, "type": "? placeholder", "action": "Replaced → 'Unknown'"},
    {"column": "diag_1", "count": 21, "pct": 0.02, "type": "? placeholder", "action": "Replaced → 'Unknown'"},
]

CLEANING_STEPS = [
    {
        "step": 1,
        "title": "Drop Useless Columns",
        "detail": "Removed weight (96.9% missing), encounter_id (unique ID  -  no predictive value), patient_nbr (patient ID  -  data leakage risk). Shape: 101,766 × 50 → 101,766 × 47.",
        "icon": "trash",
    },
    {
        "step": 2,
        "title": "Handle Missing Values",
        "detail": "Type A: '?' placeholder strings in race, payer_code, medical_specialty, diag_1–3 replaced with 'Unknown'. Type B: Genuine NaN in max_glu_serum, A1Cresult (test not performed) filled with 'Unknown'.",
        "icon": "wrench",
    },
    {
        "step": 3,
        "title": "Binarise Target Variable",
        "detail": "readmitted (3 classes: <30, >30, NO) → readmitted_binary (1 = <30, 0 = otherwise). Positive class: 11,357 (11.2%).",
        "icon": "target",
    },
    {
        "step": 4,
        "title": "Convert Age to Numeric",
        "detail": "Decade bracket strings ([60-70)) converted to midpoint values (65). Enables use as a continuous feature.",
        "icon": "hash",
    },
    {
        "step": 5,
        "title": "Map Coded ID Columns",
        "detail": "admission_type_id, discharge_disposition_id, admission_source_id converted from integer codes to readable labels via IDS_mapping.csv. Three NULL codes (6, 18, 17) added manually.",
        "icon": "map",
    },
    {
        "step": 6,
        "title": "Drop Replaced Originals",
        "detail": "age, readmitted, admission_type_id, discharge_disposition_id, admission_source_id dropped  -  superseded by cleaned replacements.",
        "icon": "scissors",
    },
]

# ─── EDA Data ─────────────────────────────────────────────────────────────────
EDA_UTILISATION_COMPARISON = [
    {"metric": "Prior Inpatient Stays", "not_readmitted": 0.562, "readmitted": 1.224, "pct_diff": 117.9},
    {"metric": "Prior ER Visits", "not_readmitted": 0.178, "readmitted": 0.357, "pct_diff": 101.0},
    {"metric": "Time in Hospital (days)", "not_readmitted": 4.349, "readmitted": 4.768, "pct_diff": 9.6},
    {"metric": "Num Medications", "not_readmitted": 15.911, "readmitted": 16.903, "pct_diff": 6.2},
    {"metric": "Num Diagnoses", "not_readmitted": 7.389, "readmitted": 7.693, "pct_diff": 4.1},
    {"metric": "Lab Procedures", "not_readmitted": 42.954, "readmitted": 44.226, "pct_diff": 3.0},
]

EDA_INPATIENT_RATE = [
    {"group": "0", "rate": 8.4, "count": 67_630},
    {"group": "1", "rate": 12.9, "count": 19_521},
    {"group": "2", "rate": 17.4, "count": 7_566},
    {"group": "3", "rate": 20.3, "count": 3_411},
    {"group": "4+", "rate": 30.7, "count": 3_638},
]

EDA_DISCHARGE_RATES = [
    {"label": "Transfer: Rehab Facility", "rate": 27.7, "count": 1_993},
    {"label": "Transfer: Inpatient Inst.", "rate": 20.9, "count": 1_184},
    {"label": "Transfer: Short-term Hospital", "rate": 16.1, "count": 2_128},
    {"label": "Transfer: SNF", "rate": 14.7, "count": 13_954},
    {"label": "Left AMA", "rate": 14.4, "count": 623},
    {"label": "Transfer: ICF", "rate": 12.8, "count": 815},
    {"label": "Home + Health Service", "rate": 12.7, "count": 12_902},
    {"label": "Discharged to Home", "rate": 9.3, "count": 60_234},
    {"label": "Transfer: Long-term Hospital", "rate": 7.3, "count": 412},
]

EDA_SPECIALTY_RATES = [
    {"specialty": "Nephrology", "rate": 15.4, "count": 1_613},
    {"specialty": "Surgery-Vascular", "rate": 13.9, "count": 533},
    {"specialty": "Psychiatry", "rate": 12.2, "count": 854},
    {"specialty": "Family/General Practice", "rate": 11.9, "count": 7_440},
    {"specialty": "Internal Medicine", "rate": 11.2, "count": 14_635},
    {"specialty": "Emergency/Trauma", "rate": 11.2, "count": 7_565},
    {"specialty": "Surgery-General", "rate": 11.0, "count": 3_099},
    {"specialty": "Pulmonology", "rate": 11.0, "count": 871},
    {"specialty": "Orthopedics", "rate": 10.8, "count": 1_400},
    {"specialty": "Cardiology", "rate": 7.9, "count": 4_200},
]

EDA_DIAG_RATES = [
    {"category": "Diabetes", "rate": 13.0, "count": 8_757},
    {"category": "Injury/Poisoning", "rate": 12.2, "count": 6_974},
    {"category": "Circulatory", "rate": 11.4, "count": 30_437},
    {"category": "Other", "rate": 11.2, "count": 23_456},
    {"category": "Genitourinary", "rate": 10.8, "count": 5_078},
    {"category": "Digestive", "rate": 10.5, "count": 9_208},
    {"category": "Neoplasms", "rate": 10.1, "count": 3_433},
    {"category": "Respiratory", "rate": 9.7, "count": 14_423},
]

EDA_CORRELATION = [
    {"feature": "number_inpatient", "corr": 0.165},
    {"feature": "number_emergency", "corr": 0.061},
    {"feature": "number_diagnoses", "corr": 0.050},
    {"feature": "time_in_hospital", "corr": 0.044},
    {"feature": "num_medications", "corr": 0.038},
    {"feature": "num_lab_procedures", "corr": 0.020},
    {"feature": "number_outpatient", "corr": 0.019},
    {"feature": "age_numeric", "corr": 0.018},
    {"feature": "num_procedures", "corr": -0.012},
]

EDA_KEY_FINDINGS = [
    {
        "rank": 1,
        "feature": "Prior Inpatient Stays",
        "finding": "2.2× higher in readmitted patients; rate rises 8% → 31% with more prior stays",
        "implication": "Strongest single feature  -  must be included",
        "icon": "activity",
    },
    {
        "rank": 2,
        "feature": "Prior ER Visits",
        "finding": "2.0× higher in readmitted patients",
        "implication": "Include as-is; combine with inpatient into 'utilisation score'",
        "icon": "alert-triangle",
    },
    {
        "rank": 3,
        "feature": "Discharge Disposition",
        "finding": "Transfer to rehab/inpatient: 21–28% readmission vs 9% for home discharge",
        "implication": "High-cardinality categorical  -  encode carefully",
        "icon": "navigation",
    },
    {
        "rank": 4,
        "feature": "Medical Specialty",
        "finding": "Nephrology (15.4%), Vascular Surgery (13.9%) vs Cardiology (7.9%)",
        "implication": "Encode with target encoding or grouping",
        "icon": "heart",
    },
    {
        "rank": 5,
        "feature": "Primary Diagnosis Category",
        "finding": "Diabetes as primary diagnosis: 13% vs 10.7% average",
        "implication": "Group ICD-9 codes into clinical categories",
        "icon": "clipboard",
    },
    {
        "rank": 6,
        "feature": "Insulin Use",
        "finding": "+2pp readmission vs non-insulin patients (53% of encounters use insulin)",
        "implication": "Binary feature or encode dosage direction",
        "icon": "droplet",
    },
]

# ─── Hypothesis Testing ───────────────────────────────────────────────────────
HYPOTHESES = [
    {
        "id": "H1",
        "title": "Prior Inpatient Utilisation",
        "research_question": "Do patients readmitted within 30 days have higher prior inpatient utilisation than those who were not?",
        "h0": "The distribution of number_inpatient is the same in both readmission groups.",
        "h1": "The distribution of number_inpatient is higher among patients readmitted within 30 days.",
        "variable": "number_inpatient",
        "test": "Mann-Whitney U",
        "test_reason": "Both groups violate normality (Shapiro-Wilk p ≈ 0, n=5,000 sample). Non-parametric test appropriate.",
        "group0_median": 0.0,
        "group1_median": 0.0,
        "group0_mean": 0.5549,
        "group1_mean": 1.2227,
        "statistic": "6.05 × 10⁸",
        "p_value": "< 0.0001",
        "effect_size": 0.165,
        "effect_type": "Cliff's delta",
        "effect_magnitude": "small",
        "decision": "Reject H₀",
        "interpretation": "Readmitted patients have significantly more prior inpatient stays (mean 1.22 vs 0.55). With 2.2× the utilisation, prior hospitalisation is the single strongest clinical signal  -  a patient's history is their future risk.",
        "color": "success",
    },
    {
        "id": "H2",
        "title": "Length of Stay",
        "research_question": "Do patients readmitted within 30 days have longer hospital stays than those not readmitted?",
        "h0": "The distribution of time_in_hospital is the same across readmission groups.",
        "h1": "Readmitted patients have longer hospital stays.",
        "variable": "time_in_hospital",
        "test": "Mann-Whitney U",
        "test_reason": "Non-normality confirmed in both groups (Shapiro-Wilk p ≈ 0). Same test selection logic as H1.",
        "group0_median": 4.0,
        "group1_median": 4.0,
        "group0_mean": 4.329,
        "group1_mean": 4.768,
        "statistic": "5.45 × 10⁸",
        "p_value": "< 0.0001",
        "effect_size": 0.044,
        "effect_type": "Cliff's delta",
        "effect_magnitude": "negligible",
        "decision": "Reject H₀",
        "interpretation": "Statistically significant, but the effect is negligible (Cliff's delta = 0.044). Length of stay is a secondary predictor  -  useful in a model but not a clinical differentiator on its own.",
        "color": "warning",
    },
    {
        "id": "H3",
        "title": "Discharge Disposition",
        "research_question": "Is discharge disposition associated with 30-day readmission?",
        "h0": "Discharge disposition and readmitted_binary are independent.",
        "h1": "Discharge disposition and readmitted_binary are associated.",
        "variable": "discharge_disposition",
        "test": "Chi-Square Test of Independence",
        "test_reason": "Both variables are categorical. Contingency table (13×2) verified: 0 cells with expected count < 5.",
        "group0_median": None,
        "group1_median": None,
        "group0_mean": None,
        "group1_mean": None,
        "statistic": "1,225.26",
        "p_value": "< 0.0001",
        "effect_size": 0.111,
        "effect_type": "Cramér's V",
        "effect_magnitude": "small",
        "decision": "Reject H₀",
        "interpretation": "Strong statistical evidence of association. Transfers to rehab/inpatient facilities show 21–28% readmission rates vs 9.3% for home discharge. Discharge disposition is one of the strongest operational risk indicators.",
        "color": "success",
    },
    {
        "id": "H4",
        "title": "Medication Change",
        "research_question": "Is medication change status associated with 30-day readmission?",
        "h0": "Change status and readmitted_binary are independent.",
        "h1": "Medication change is associated with 30-day readmission.",
        "variable": "change",
        "test": "Chi-Square Test of Independence",
        "test_reason": "Binary categorical variable. Contingency table (2×2): 0 cells with expected count < 5.",
        "group0_median": None,
        "group1_median": None,
        "group0_mean": None,
        "group1_mean": None,
        "statistic": "34.13",
        "p_value": "< 0.0001",
        "effect_size": 0.018,
        "effect_type": "Cramér's V",
        "effect_magnitude": "negligible",
        "decision": "Reject H₀",
        "interpretation": "Statistically significant but effect is negligible (Cramér's V = 0.018). Medication change may reflect clinical complexity more than direct causation  -  useful as a binary indicator in modelling.",
        "color": "warning",
    },
]

# ─── Machine Learning Models ──────────────────────────────────────────────────
MODEL_COMPARISON = [
    {
        "rank": 1,
        "name": "LightGBM",
        "recommended": True,
        "accuracy": 0.6813,
        "precision": 0.1884,
        "recall": 0.5435,
        "f1": 0.2798,
        "roc_auc": 0.6745,
        "pr_auc": 0.2403,
        "confusion_matrix": [[12307, 5299], [1033, 1230]],
        "color": "#00B4D8",
        "why_selected": "Best PR-AUC and Recall trade-off with competitive ROC-AUC. Efficient on wide encoded datasets. Handles class imbalance via class_weight='balanced'.",
        "strengths": ["Fastest training on large datasets", "Handles sparse OHE features efficiently", "Strong Recall (54.4%)  -  catches more high-risk patients", "Competitive PR-AUC = 0.2403"],
        "limitations": ["Lower accuracy than Random Forest", "Less interpretable than Logistic Regression"],
    },
    {
        "rank": 2,
        "name": "XGBoost",
        "recommended": True,
        "accuracy": 0.6865,
        "precision": 0.1921,
        "recall": 0.5466,
        "f1": 0.2843,
        "roc_auc": 0.6804,
        "pr_auc": 0.2403,
        "confusion_matrix": [[12404, 5202], [1026, 1237]],
        "color": "#2DC653",
        "why_selected": "Highest ROC-AUC (0.6804) and best F1 (0.2843) among all models. Scale_pos_weight applied to address class imbalance directly.",
        "strengths": ["Highest ROC-AUC = 0.6804", "Best F1-Score = 0.2843", "Robust gradient boosting on tabular data", "Scale_pos_weight compensates for imbalance"],
        "limitations": ["Slower training than LightGBM", "Requires careful hyperparameter tuning"],
    },
    {
        "rank": 3,
        "name": "Random Forest",
        "recommended": False,
        "accuracy": 0.7598,
        "precision": 0.2175,
        "recall": 0.4269,
        "f1": 0.2881,
        "roc_auc": 0.6781,
        "pr_auc": 0.2265,
        "confusion_matrix": [[14130, 3476], [1297, 966]],
        "color": "#718096",
        "why_selected": "Highest accuracy (76%) but lower Recall. Better for precision-focused use cases.",
        "strengths": ["Highest accuracy = 75.98%", "Best precision = 21.75%", "Robust to overfitting"],
        "limitations": ["Lowest Recall (42.7%)  -  misses more high-risk patients", "Slower than gradient boosting models"],
    },
    {
        "rank": 4,
        "name": "Logistic Regression",
        "recommended": False,
        "accuracy": 0.6644,
        "precision": 0.1794,
        "recall": 0.5444,
        "f1": 0.2698,
        "roc_auc": 0.6555,
        "pr_auc": 0.2155,
        "confusion_matrix": [[11969, 5637], [1031, 1232]],
        "color": "#A0AEC0",
        "why_selected": "Strong interpretable baseline. Good Recall but lowest ROC-AUC. Best for academic explanation.",
        "strengths": ["Highest interpretability", "Coefficient-based clinical reasoning", "Good Recall (54.4%)"],
        "limitations": ["Lowest ROC-AUC = 0.6555", "Lowest PR-AUC = 0.2155", "Assumes linearity"],
    },
]

TOP_FEATURES = [
    {"feature": "num_lab_procedures", "importance": 834, "pct": 100.0, "group": "Clinical"},
    {"feature": "num_medications", "importance": 670, "pct": 80.3, "group": "Clinical"},
    {"feature": "time_in_hospital", "importance": 489, "pct": 58.6, "group": "Clinical"},
    {"feature": "age_numeric", "importance": 366, "pct": 43.9, "group": "Demographic"},
    {"feature": "number_diagnoses", "importance": 293, "pct": 35.1, "group": "Clinical"},
    {"feature": "num_procedures", "importance": 273, "pct": 32.7, "group": "Clinical"},
    {"feature": "number_inpatient", "importance": 259, "pct": 31.1, "group": "Utilisation"},
    {"feature": "number_outpatient", "importance": 129, "pct": 15.5, "group": "Utilisation"},
    {"feature": "medical_specialty_Unknown", "importance": 125, "pct": 15.0, "group": "Clinical"},
    {"feature": "number_emergency", "importance": 111, "pct": 13.3, "group": "Utilisation"},
    {"feature": "discharge_disposition_Home", "importance": 100, "pct": 12.0, "group": "Discharge"},
    {"feature": "insulin_Steady", "importance": 80, "pct": 9.6, "group": "Medication"},
    {"feature": "change_Ch", "importance": 66, "pct": 7.9, "group": "Medication"},
]

IMBALANCE_NOTE = (
    "The 8:1 class imbalance means Accuracy is a misleading metric. "
    "A naive model predicting 'never readmitted' achieves 88.8% accuracy with zero clinical value. "
    "Recall and PR-AUC are the appropriate primary metrics for this clinical risk-detection task, "
    "where missing a high-risk patient (false negative) is far more costly than a false alarm."
)

# ─── Predict page  -  form fields ───────────────────────────────────────────────
PREDICT_FEATURES = [
    # (field_id, label, field_type, options_or_range, default, help_text)
    ("age_numeric", "Patient Age", "number", [18, 100], 65, "Age in years"),
    ("time_in_hospital", "Length of Stay (days)", "number", [1, 14], 4, "Current inpatient days"),
    ("number_inpatient", "Prior Inpatient Stays (past year)", "number", [0, 20], 0, "Number of inpatient admissions in the past year"),
    ("number_emergency", "Prior ER Visits (past year)", "number", [0, 20], 0, "Number of emergency visits in the past year"),
    ("number_outpatient", "Prior Outpatient Visits (past year)", "number", [0, 40], 0, "Outpatient visits in the past year"),
    ("num_medications", "Number of Medications", "number", [1, 80], 15, "Total distinct medications administered"),
    ("num_lab_procedures", "Number of Lab Procedures", "number", [1, 132], 43, "Lab tests performed during stay"),
    ("num_procedures", "Number of Procedures", "number", [0, 6], 1, "Number of procedures (not lab) performed"),
    ("number_diagnoses", "Number of Diagnoses", "number", [1, 16], 7, "Total number of diagnoses entered"),
    ("admission_type", "Admission Type", "select",
     ["Emergency", "Urgent", "Elective", "Not Available"], "Emergency", "How the patient was admitted"),
    ("discharge_disposition", "Discharge Disposition", "select",
     ["Discharged to home", "Discharged/transferred to SNF",
      "Discharged/transferred to home with home health service",
      "Discharged/transferred to another rehab fac including rehab units of a hospital",
      "Left AMA", "Other"], "Discharged to home", "Where patient is being discharged to"),
    ("insulin", "Insulin Status", "select", ["No", "Steady", "Up", "Down"], "Steady", "Insulin dosage during stay"),
    ("change", "Medication Change", "select", ["Ch", "No"], "Ch", "Was any diabetes medication changed?"),
    ("diabetesMed", "On Diabetes Medication", "select", ["Yes", "No"], "Yes", "Is patient on any diabetes medication?"),
    ("gender", "Gender", "select", ["Female", "Male"], "Female", "Patient gender"),
]