from math import isfinite
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

model_path = Path(__file__).with_name("extraalearn_lead_conversion.joblib")
model = joblib.load(model_path)
feature_names = model.feature_names_in_.tolist()
conversion_index = model.classes_.tolist().index(1)

numeric_features = {
    "age",
    "website_visits",
    "time_spent_on_website",
    "page_views_per_visit",
}


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    lead = request.get_json(silent=True)
    if not isinstance(lead, dict):
        return jsonify({"error": "Send one lead as a JSON object."}), 400

    missing = sorted(set(feature_names) - lead.keys())
    unexpected = sorted(lead.keys() - set(feature_names))
    if missing or unexpected:
        return jsonify({
            "error": "Provide the original predictor fields.",
            "missing_fields": missing,
            "unexpected_fields": unexpected,
        }), 400

    for name in feature_names:
        value = lead[name]
        if name in numeric_features:
            if type(value) not in (int, float) or not isfinite(value) or value < 0:
                return jsonify({"error": f"{name} must be a non-negative number."}), 400
        elif not isinstance(value, str) or not value.strip():
            return jsonify({"error": f"{name} must be a non-empty string."}), 400

    predictors = pd.DataFrame([lead], columns=feature_names)
    prediction = int(model.predict(predictors)[0])
    probability = float(model.predict_proba(predictors)[0, conversion_index])

    return jsonify({
        "prediction": prediction,
        "conversion_probability": probability,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
