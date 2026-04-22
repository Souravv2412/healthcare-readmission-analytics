# utils/model_utils.py
"""
Model utilities for prediction.
Loads trained model artifacts if available; falls back to a rule-based
risk scorer derived from EDA findings so the predict page always works.
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path


MODEL_DIR = Path(__file__).parent.parent / "models"


def _load_artifact(filename):
    """Try to load a pickle artifact; return None if not found."""
    path = MODEL_DIR / filename
    if path.exists():
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None
    return None


def load_model_metadata():
    """Load metadata.json if it exists."""
    path = MODEL_DIR / "metadata.json"
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def predict_readmission(form_data: dict) -> dict:
    """
    Returns a prediction dict:
      {
        'probability': float (0–1),
        'risk_band': str,
        'risk_label': str,
        'risk_color': str,
        'key_drivers': list[str],
        'model_used': str,
      }

    Tries to use the trained LightGBM pipeline first.
    Falls back to an evidence-based rule scorer when the model is absent.
    """
    lgbm = _load_artifact("lightgbm_model.pkl")
    preprocessor = _load_artifact("preprocessor.pkl")

    if lgbm is not None and preprocessor is not None:
        return _predict_with_model(lgbm, preprocessor, form_data, "LightGBM")

    # Fallback: EDA-derived risk score
    return _rule_based_score(form_data)


def _predict_with_model(model, preprocessor, form_data, model_name):
    """Use fitted sklearn pipeline to predict."""
    import pandas as pd

    row = pd.DataFrame([form_data])
    try:
        X = preprocessor.transform(row)
        prob = float(model.predict_proba(X)[0, 1])
    except Exception:
        return _rule_based_score(form_data)

    band, label, color = _risk_band(prob)
    return {
        "probability": round(prob, 4),
        "probability_pct": round(prob * 100, 1),
        "risk_band": band,
        "risk_label": label,
        "risk_color": color,
        "key_drivers": _top_drivers(form_data),
        "model_used": model_name,
    }


def _rule_based_score(form_data: dict) -> dict:
    """
    Evidence-based risk score derived from EDA & hypothesis testing.
    Weights sourced from feature importance and readmission rate differentials.
    """
    score = 0.0

    # Prior utilisation  -  dominant signal
    inpatient = int(form_data.get("number_inpatient", 0))
    emergency = int(form_data.get("number_emergency", 0))
    score += min(inpatient, 5) * 0.07   # up to +0.35
    score += min(emergency, 5) * 0.04   # up to +0.20

    # Discharge disposition
    discharge = str(form_data.get("discharge_disposition", ""))
    high_risk_discharge = ["rehab", "inpatient", "short term", "snf", "icf"]
    if any(k in discharge.lower() for k in high_risk_discharge):
        score += 0.10
    elif "home health" in discharge.lower():
        score += 0.03

    # Insulin  -  proxy for disease severity
    insulin = str(form_data.get("insulin", "No"))
    if insulin in ("Steady", "Up", "Down"):
        score += 0.04
    if insulin == "Up":
        score += 0.02

    # Clinical complexity
    meds = int(form_data.get("num_medications", 15))
    diags = int(form_data.get("number_diagnoses", 7))
    los = int(form_data.get("time_in_hospital", 4))
    score += max(0, (meds - 15) / 100)
    score += max(0, (diags - 7) / 50)
    score += max(0, (los - 4) / 50)

    # Medication change
    if str(form_data.get("change", "No")) == "Ch":
        score += 0.02

    # Admission type
    if str(form_data.get("admission_type", "")) == "Emergency":
        score += 0.01

    # Baseline  -  overall positive class rate
    base = 0.112
    prob = min(base + score, 0.92)

    band, label, color = _risk_band(prob)
    return {
        "probability": round(prob, 4),
        "probability_pct": round(prob * 100, 1),
        "risk_band": band,
        "risk_label": label,
        "risk_color": color,
        "key_drivers": _top_drivers(form_data),
        "model_used": "Evidence-Based Risk Score (LightGBM artifact not found)",
    }


def _risk_band(prob: float):
    if prob < 0.10:
        return "low", "Low Risk", "#2DC653"
    elif prob < 0.20:
        return "moderate", "Moderate Risk", "#F4A261"
    elif prob < 0.35:
        return "high", "High Risk", "#E76F51"
    else:
        return "very-high", "Very High Risk", "#E84855"


def _top_drivers(form_data: dict) -> list:
    """Return a short list of the most influential input factors."""
    drivers = []
    inpatient = int(form_data.get("number_inpatient", 0))
    emergency = int(form_data.get("number_emergency", 0))
    discharge = str(form_data.get("discharge_disposition", ""))
    insulin = str(form_data.get("insulin", "No"))
    meds = int(form_data.get("num_medications", 15))
    diags = int(form_data.get("number_diagnoses", 7))

    if inpatient >= 2:
        drivers.append(f"Prior inpatient stays: {inpatient} (strongly elevated risk)")
    elif inpatient == 1:
        drivers.append("1 prior inpatient stay (moderate elevation)")

    if emergency >= 2:
        drivers.append(f"Prior ER visits: {emergency} (high utilisation signal)")
    elif emergency == 1:
        drivers.append("1 prior ER visit (moderate signal)")

    high_risk_discharge = ["rehab", "inpatient", "short term", "snf", "icf"]
    if any(k in discharge.lower() for k in high_risk_discharge):
        drivers.append(f"Discharge to '{discharge}'  -  elevated readmission category")

    if insulin in ("Up", "Down"):
        drivers.append(f"Insulin dose change ({insulin})  -  active disease management")

    if meds > 20:
        drivers.append(f"High medication burden ({meds} medications)")

    if diags > 9:
        drivers.append(f"High diagnostic complexity ({diags} diagnoses)")

    if not drivers:
        drivers.append("No strongly elevated individual risk factors detected")

    return drivers