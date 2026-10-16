# Credit Card Fraud Detection

A small web application using a trained scikit-learn Random Forest classifier. The frontend is a static HTML page and `/api/predict` is a Vercel Python Function.

## Files

- `index.html` — transaction feature form and prediction display
- `api/predict.py` — loads `fraud_model.pkl` and returns a prediction
- `fraud_model.pkl` — trained model exported from Google Colab
- `requirements.txt` — Python dependencies
- `vercel.json` — Vercel function configuration

## Run locally

Use Python 3.11 or 3.12 in a virtual environment, then install:

```bash
pip install -r requirements.txt
```

The API file is intended to run as a Vercel Function; opening `index.html` directly on its own will not make the API work locally.

## Deploy to Vercel

1. Push this whole folder to a GitHub repository.
2. In Vercel, choose **Add New → Project** and import that repository.
3. Keep the project root at the repository root and deploy.
4. Open the deployed URL and test with the demo values to confirm the API responds.

## Feature order and model compatibility

The API sends values in this exact order: `Time`, `V1` through `V28`, `Amount`. The provided model expects 30 features and was loaded as a scikit-learn `RandomForestClassifier`. `scikit-learn==1.6.1` is pinned to match the version used to serialize the model.

## Important limitations

- All-zero demo values are only an integration test, not a realistic transaction.
- `V1`–`V28` are transformed features from the common credit-card fraud dataset. They cannot generally be filled from ordinary fields like merchant, card number, or location.
- This is a demonstration project, not a production fraud-screening system. Evaluate the model on a held-out dataset and review precision, recall, confusion matrix, and false-positive/false-negative rates before any real use.
- Do not upload real cardholder data, card numbers, CVV, or other sensitive financial information to this demo.
