# app.py  -  Main Flask application
# Predicting 30-Day Hospital Readmissions in Diabetic Patients
# Diabetes 130-US Hospitals Dataset | University Final Project

import os
from flask import Flask, render_template, request, jsonify

from utils.constants import (
    PROJECT_TITLE, PROJECT_SUBTITLE, DATASET_STATS,
    AUDIT_COLUMN_GROUPS, MISSING_VALUES, CLEANING_STEPS,
    EDA_UTILISATION_COMPARISON, EDA_INPATIENT_RATE, EDA_DISCHARGE_RATES,
    EDA_SPECIALTY_RATES, EDA_DIAG_RATES, EDA_CORRELATION, EDA_KEY_FINDINGS,
    HYPOTHESES, MODEL_COMPARISON, TOP_FEATURES, IMBALANCE_NOTE,
    PREDICT_FEATURES,
)
from utils.model_utils import predict_readmission

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "healthcare-readmission-2024")


# ─── Context injected into every template ─────────────────────────────────────
@app.context_processor
def inject_globals():
    return {
        "project_title": PROJECT_TITLE,
        "project_subtitle": PROJECT_SUBTITLE,
        "nav_items": [
            {"id": "home",       "label": "Dashboard",         "icon": "home",         "url": "/"},
            {"id": "audit",      "label": "Data Audit",        "icon": "search",       "url": "/audit"},
            {"id": "cleaning",   "label": "Data Cleaning",     "icon": "filter",       "url": "/cleaning"},
            {"id": "eda",        "label": "EDA",               "icon": "bar-chart-2",  "url": "/eda"},
            {"id": "hypothesis", "label": "Hypothesis Tests",  "icon": "check-square", "url": "/hypothesis"},
            {"id": "models",     "label": "ML Models",         "icon": "cpu",          "url": "/models"},
            {"id": "predict",    "label": "Risk Predictor",    "icon": "activity",     "url": "/predict"},
            {"id": "about",      "label": "Methodology",       "icon": "book-open",    "url": "/about"},
        ],
    }


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    lgbm = next((m for m in MODEL_COMPARISON if m["name"] == "LightGBM"), None)
    xgb  = next((m for m in MODEL_COMPARISON if m["name"] == "XGBoost"),  None)
    return render_template(
        "index.html",
        active="home",
        stats=DATASET_STATS,
        lgbm=lgbm,
        xgb=xgb,
        eda_findings=EDA_KEY_FINDINGS[:4],
        hypotheses=HYPOTHESES,
    )


@app.route("/audit")
def audit():
    return render_template(
        "audit.html",
        active="audit",
        stats=DATASET_STATS,
        column_groups=AUDIT_COLUMN_GROUPS,
        missing_values=MISSING_VALUES,
    )


@app.route("/cleaning")
def cleaning():
    return render_template(
        "cleaning.html",
        active="cleaning",
        steps=CLEANING_STEPS,
        stats=DATASET_STATS,
    )


@app.route("/eda")
def eda():
    return render_template(
        "eda.html",
        active="eda",
        stats=DATASET_STATS,
        utilisation=EDA_UTILISATION_COMPARISON,
        inpatient_rate=EDA_INPATIENT_RATE,
        discharge_rates=EDA_DISCHARGE_RATES,
        specialty_rates=EDA_SPECIALTY_RATES,
        diag_rates=EDA_DIAG_RATES,
        correlation=EDA_CORRELATION,
        key_findings=EDA_KEY_FINDINGS,
    )


@app.route("/hypothesis")
def hypothesis():
    return render_template(
        "hypothesis.html",
        active="hypothesis",
        hypotheses=HYPOTHESES,
    )


@app.route("/models")
def models():
    return render_template(
        "models.html",
        active="models",
        model_comparison=MODEL_COMPARISON,
        top_features=TOP_FEATURES,
        imbalance_note=IMBALANCE_NOTE,
        stats=DATASET_STATS,
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None
    form_values = {}

    if request.method == "POST":
        form_values = request.form.to_dict()
        # Cast numeric fields
        numeric_fields = [
            "age_numeric", "time_in_hospital", "number_inpatient",
            "number_emergency", "number_outpatient", "num_medications",
            "num_lab_procedures", "num_procedures", "number_diagnoses",
        ]
        for f in numeric_fields:
            try:
                form_values[f] = int(form_values.get(f, 0))
            except (ValueError, TypeError):
                form_values[f] = 0

        result = predict_readmission(form_values)

    return render_template(
        "predict.html",
        active="predict",
        features=PREDICT_FEATURES,
        result=result,
        form_values=form_values,
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        active="about",
        stats=DATASET_STATS,
    )


# ─── API endpoint for chart data ──────────────────────────────────────────────

@app.route("/api/chart/<chart_id>")
def chart_data(chart_id):
    data_map = {
        "inpatient_rate":  EDA_INPATIENT_RATE,
        "discharge_rates": EDA_DISCHARGE_RATES,
        "specialty_rates": EDA_SPECIALTY_RATES,
        "diag_rates":      EDA_DIAG_RATES,
        "correlation":     EDA_CORRELATION,
        "utilisation":     EDA_UTILISATION_COMPARISON,
        "top_features":    TOP_FEATURES[:12],
        "model_metrics":   [
            {
                "name": m["name"],
                "recall": m["recall"],
                "roc_auc": m["roc_auc"],
                "pr_auc": m["pr_auc"],
                "f1": m["f1"],
                "accuracy": m["accuracy"],
            }
            for m in MODEL_COMPARISON
        ],
    }
    payload = data_map.get(chart_id)
    if payload is None:
        return jsonify({"error": "unknown chart"}), 404
    return jsonify(payload)


# ─── Error handlers ───────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)