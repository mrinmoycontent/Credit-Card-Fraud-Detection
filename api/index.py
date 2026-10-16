
import json
import os
import joblib
import numpy as np
from http.server import BaseHTTPRequestHandler

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "fraud_model.pkl"
)

_model = None

FEATURES = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount"]
)

FRAUD_THRESHOLD = 0.50
REVIEW_THRESHOLD = 0.30
MAX_TRANSACTIONS = 500


def get_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "fraud_model.pkl was not found in the repository root."
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def score_one(model, item):
    if not isinstance(item, dict):
        raise ValueError("Each transaction must be an object.")

    values = item.get("features", item)

    if not isinstance(values, dict):
        raise ValueError("Each transaction must contain a features object.")

    missing = [
        name for name in FEATURES
        if name not in values
    ]

    if missing:
        raise ValueError(
            "Missing features: " + ", ".join(missing)
        )

    try:
        row = [float(values[name]) for name in FEATURES]
    except (TypeError, ValueError):
        raise ValueError(
            "Every feature must be a valid number."
        )

    if not np.all(np.isfinite(row)):
        raise ValueError(
            "Feature values must be finite numbers."
        )

    # Keep the existing trained model; do not retrain it.
    prediction = int(model.predict([row])[0])

    fraud_probability = None

    if hasattr(model, "predict_proba"):
        classes = list(model.classes_)

        if 1 in classes:
            probabilities = model.predict_proba([row])[0]
            fraud_probability = float(
                probabilities[classes.index(1)]
            )

    if fraud_probability is None:
        risk = (
            "POTENTIAL FRAUD"
            if prediction == 1
            else "LIKELY LEGITIMATE"
        )
    elif fraud_probability >= FRAUD_THRESHOLD:
        risk = "POTENTIAL FRAUD"
    elif fraud_probability >= REVIEW_THRESHOLD:
        risk = "REVIEW REQUIRED"
    else:
        risk = "LIKELY LEGITIMATE"

    result = {
        "transaction_id": str(
            item.get(
                "transaction_id",
                item.get("Demo_Transaction_ID", "")
            )
        ),
        "amount": float(values.get("Amount", 0)),
        "prediction": prediction,
        "risk_assessment": risk,
        "label": (
            "Potential Fraud"
            if prediction == 1
            else "Likely Legitimate"
        ),
        "fraud_probability": fraud_probability,
    }

    actual = item.get(
        "Class",
        item.get("actual_label")
    )

    if actual is not None and str(actual).strip() != "":
        try:
            result["actual_label"] = (
                "FRAUD"
                if int(float(actual)) == 1
                else "LEGITIMATE"
            )
        except (TypeError, ValueError):
            pass

    return result


class handler(BaseHTTPRequestHandler):

    def _send(self, status, payload):
        body = json.dumps(
            payload,
            allow_nan=False
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.send_header("Cache-Control", "no-store")
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )
        self.end_headers()

        if status != 204:
            self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        self._send(200, {
            "status": "ok",
            "message": "FraudWatch API is running.",
            "required_features": FEATURES,
            "max_transactions_per_request": MAX_TRANSACTIONS
        })

    def do_POST(self):
        try:
            length = int(
                self.headers.get("Content-Length", "0")
            )

            if length <= 0 or length > 5_000_000:
                self._send(400, {
                    "error": "Request body is empty or too large."
                })
                return

            raw_body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw_body)

            if not isinstance(payload, dict):
                self._send(400, {
                    "error": "Request body must be a JSON object."
                })
                return

            model = get_model()

            # Single-transaction prediction.
            if "features" in payload:
                result = score_one(model, payload)
                result["note"] = (
                    "Demo model output only. "
                    "Do not use for real financial decisions."
                )
                self._send(200, result)
                return

            # Batch predictions for CSV analysis.
            transactions = payload.get("transactions")

            if not isinstance(transactions, list) or not transactions:
                self._send(400, {
                    "error": (
                        "Send a features object or a non-empty "
                        "transactions list."
                    )
                })
                return

            if len(transactions) > MAX_TRANSACTIONS:
                self._send(400, {
                    "error": (
                        f"Send no more than {MAX_TRANSACTIONS} "
                        "transactions per request."
                    )
                })
                return

            results = [
                score_one(model, item)
                for item in transactions
            ]

            self._send(200, {
                "results": results,
                "count": len(results),
                "note": (
                    "Demo model output only. "
                    "Do not use for real financial decisions."
                )
            })

        except json.JSONDecodeError:
            self._send(400, {
                "error": "Request body must be valid JSON."
            })

        except ValueError as exc:
            self._send(400, {
                "error": str(exc)
            })

        except Exception:
            self._send(500, {
                "error": (
                    "Prediction failed. Check Vercel function logs "
                    "and model/dependency compatibility."
                )
            })
