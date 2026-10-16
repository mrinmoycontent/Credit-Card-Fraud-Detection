import json
import os
import joblib
import numpy as np
from http.server import BaseHTTPRequestHandler

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fraud_model.pkl")
_model = None

FEATURES = [
    "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
    "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18",
    "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27",
    "V28", "Amount"
]

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

class handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        self._send(200, {
            "status": "ok",
            "message": "Credit Card Fraud Detection API is running.",
            "required_features": FEATURES
        })

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100_000:
                return self._send(400, {"error": "Please send a valid JSON request."})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            values = payload.get("features")

            if not isinstance(values, dict):
                return self._send(400, {"error": "Expected a 'features' object containing all 30 feature values."})

            missing = [name for name in FEATURES if name not in values]
            if missing:
                return self._send(400, {"error": "Missing features: " + ", ".join(missing)})

            try:
                row = [float(values[name]) for name in FEATURES]
            except (TypeError, ValueError):
                return self._send(400, {"error": "Every feature must be a valid number."})

            if not np.all(np.isfinite(row)):
                return self._send(400, {"error": "Feature values must be finite numbers."})

            model = get_model()
            prediction = int(model.predict([row])[0])
            probabilities = getattr(model, "predict_proba", None)
            fraud_probability = None
            if probabilities is not None:
                classes = list(model.classes_)
                if 1 in classes:
                    fraud_probability = float(probabilities([row])[0][classes.index(1)])

            self._send(200, {
                "prediction": prediction,
                "label": "Potential Fraud" if prediction == 1 else "Likely Legitimate",
                "fraud_probability": fraud_probability,
                "note": "This is a machine-learning demo, not a financial decision system. Validate the model before real-world use."
            })
        except json.JSONDecodeError:
            self._send(400, {"error": "Request body must be valid JSON."})
        except Exception:
            self._send(500, {"error": "Prediction failed. Check the deployment logs and model compatibility."})
