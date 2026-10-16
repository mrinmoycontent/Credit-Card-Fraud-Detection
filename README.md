
# FraudWatch — Credit Card Fraud Detection Dashboard

FraudWatch is a machine-learning-powered credit card fraud detection dashboard that analyzes transaction records using a trained Random Forest Classifier. It generates fraud probability scores, classifies transaction risk, and provides dashboard analytics to help users explore potential fraudulent activity.

The project demonstrates how machine learning can be integrated into a web application to support transaction analysis, batch prediction, and model evaluation.

## About the Project

Credit card fraud detection is a classification problem in which a model attempts to distinguish fraudulent transactions from legitimate ones. Because fraudulent transactions are rare in real-world datasets, evaluating a model requires more than looking at accuracy alone.

FraudWatch combines a web-based dashboard with a trained machine learning model. Users can explore demo transactions, inspect individual predictions, upload a CSV file for batch analysis, and evaluate predictions against actual labels when those labels are available.

## Live Demo

**Live Application:** https://credit-card-fraud-detection-inky.vercel.app/

**GitHub Repository:** https://github.com/mrinmoycontent/Credit-Card-Fraud-Detection

## Key Features

- **Interactive dashboard:** View transaction counts and risk classifications for the active dataset.
- **Transaction inspection:** Select an individual transaction to review its amount, risk assessment, fraud probability, model prediction, and available actual label.
- **CSV batch analysis:** Upload a supported CSV file and generate predictions for multiple transactions.
- **Fraud probability scoring:** View the model's estimated fraud probability for each transaction.
- **Risk classification:** Group predictions into potential fraud, review required, and likely legitimate categories.
- **Model evaluation:** Calculate accuracy, precision, recall, and F1 score when valid actual labels are supplied.
- **Confusion matrix:** Compare actual transaction labels with model predictions.
- **Downloadable results:** Export CSV prediction results for further analysis.
- **Demo dataset:** Explore the dashboard without preparing a dataset from scratch.
- **Responsive interface:** Use the dashboard on desktop and smaller screens.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Machine learning | Random Forest Classifier |
| Machine learning library | Python, scikit-learn |
| Backend API | Python serverless function |
| Model storage | Serialized scikit-learn model (`fraud_model.pkl`) |
| Hosting and deployment | Vercel |
| Version control | Git and GitHub |
| Dataset | Kaggle Credit Card Fraud Detection dataset |

## Model Information

| Property | Details |
|---|---|
| Algorithm | Random Forest Classifier |
| Dataset | Kaggle Credit Card Fraud Detection |
| Dataset records | 284,807 |
| Fraud cases in dataset | 492 |
| Input features | 30 |
| Feature structure | `Time`, `V1`–`V28`, `Amount` |
| Model artifact | `fraud_model.pkl` |

The dataset contains anonymized transaction features. Features `V1` through `V28` are transformed variables, so they cannot generally be reconstructed from ordinary transaction details such as merchant name, card number, or location.

### Reported Model Performance

The following are the model performance figures documented for this project.

| Metric | Reported value |
|---|---:|
| Accuracy | 99.96% |
| Precision | 95% |
| Recall | 80% |
| F1 score | 87% |

These figures should be interpreted in the context of the dataset and evaluation procedure. They are documented project metrics, not a guarantee of performance on new or real-world transactions. Accuracy can be misleading when fraudulent transactions make up a very small proportion of the dataset.

For a rigorous evaluation, calculate these metrics on a held-out test set that was not used to train the model.

## How FraudWatch Works

The application follows this workflow:

1. **CSV upload or demo data:** Load the included demo transactions or upload a compatible CSV file.
2. **Data processing:** Validate the required feature columns and prepare transaction inputs.
3. **Random Forest model:** Send the transaction features to the prediction API.
4. **Fraud probability:** Retrieve the model's fraud probability estimate.
5. **Risk classification:** Assign a risk category using the configured probability thresholds.
6. **Dashboard analytics:** Display transaction predictions, summary counts, evaluation metrics, and downloadable results.

```text
CSV Upload or Demo Data
          |
          v
    Data Processing
          |
          v
   Prediction API
          |
          v
   Random Forest Model
          |
          v
    Fraud Probability
          |
          v
    Risk Classification
          |
          v
   Dashboard Analytics
          |
          v
   Results CSV Export
```

## Fraud Probability Thresholds

FraudWatch uses the following probability thresholds to organize model predictions.

| Fraud probability | Classification | Interpretation |
|---|---|---|
| 50% or higher | Potential Fraud | Flag for further investigation |
| 30% to below 50% | Review Required | Review the transaction |
| Below 30% | Likely Legitimate | Lower model-estimated fraud risk |

These categories are dashboard rules applied to model probabilities. They are not proof that a transaction is fraudulent or legitimate, and the thresholds should be validated before operational use.

## CSV Upload Requirements

The CSV analysis feature expects the following 30 numerical input columns:

- `Time`
- `V1` through `V28`
- `Amount`

The following additional columns are optional:

| Column | Purpose |
|---|---|
| `Demo_Transaction_ID` or `Transaction ID` | Identifies a transaction in the results |
| `Class` | Supplies the actual label for model evaluation |

For the `Class` column:

- `0` represents a legitimate transaction.
- `1` represents a fraudulent transaction.

The dashboard currently limits an upload to 500 data rows per file.

### Important CSV Notes

- Include the required feature columns with their expected names.
- Ensure the required feature values are numeric and populated.
- Use the same feature definitions and preprocessing expected by the trained model.
- Do not include sensitive cardholder information.
- The optional `Class` column is used for evaluation when valid labels are available; it should not be treated as a prediction supplied by the model.

## Model Evaluation

When the uploaded CSV contains valid actual labels, FraudWatch calculates:

- **Accuracy:** The proportion of evaluated transactions classified correctly.
- **Precision:** The proportion of transactions predicted as fraud that are actually fraud.
- **Recall:** The proportion of actual fraudulent transactions identified by the model.
- **F1 score:** The harmonic mean of precision and recall.
- **Confusion matrix:** The counts of true positives, true negatives, false positives, and false negatives.

These evaluation results are calculated from the uploaded labeled transactions. They may differ from the reported model performance figures above because the dataset, sample size, and evaluation conditions can differ.

## Project Structure

The repository contains the dashboard, model artifact, API code, and deployment configuration.

```text
Credit-Card-Fraud-Detection/
├── api/
│   └── index.py
├── index.html
├── demo_transactions.csv
├── fraud_model.pkl
├── requirements.txt
├── vercel.json
└── README.md
```

- `index.html` — Dashboard interface, transaction inspection, CSV analysis, and client-side JavaScript.
- `api/index.py` — Python prediction API that loads the saved model and processes prediction requests.
- `demo_transactions.csv` — Demo transaction records used by the dashboard.
- `fraud_model.pkl` — Serialized trained Random Forest model.
- `requirements.txt` — Python dependencies required by the API.
- `vercel.json` — Vercel deployment and routing configuration.
- `README.md` — Project documentation.

## Running the Project Locally

### Prerequisites

- Python 3.11 or 3.12
- Git
- A compatible Python environment
- The project source files and trained model

### 1. Clone the repository

```bash
git clone https://github.com/mrinmoycontent/Credit-Card-Fraud-Detection.git
cd Credit-Card-Fraud-Detection
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

The API is configured for Vercel's serverless environment. Opening `index.html` directly in a browser will not make the `/api` endpoint available.

For local testing, use Vercel's development environment if it is compatible with the installed dependencies and project configuration:

```bash
npm install -g vercel
vercel dev
```

Then open the local URL reported by the Vercel CLI.

## Deploying to Vercel

1. Push the project files to the GitHub repository.
2. Sign in to Vercel.
3. Import the `Credit-Card-Fraud-Detection` repository as a new project.
4. Keep the project root set to the repository root.
5. Confirm the Python dependencies and serverless function configuration are present.
6. Deploy the application.
7. Open the deployed URL and test demo predictions.
8. Upload a compatible CSV file and verify that the dashboard displays results.

If the API returns an error, review the Vercel deployment logs and confirm that the model artifact and required dependencies are available to the serverless function.

## Future Enhancements

Potential improvements for future versions include:

- Real-time transaction monitoring.
- Deep learning models for fraud detection.
- Explainable AI using SHAP or similar methods.
- User authentication and access control.
- Email or SMS fraud alerts.
- Model comparison and evaluation reports.
- Improved monitoring for model drift and changing fraud patterns.
- Configurable risk thresholds.
- More detailed reporting and data visualization.

These are proposed enhancements and are not necessarily implemented in the current application.

## Limitations and Responsible Use

- FraudWatch is a portfolio and demonstration project, not a production financial screening system.
- A high accuracy score does not establish that the model reliably identifies rare fraudulent transactions.
- Predictions depend on the quality and compatibility of the supplied features.
- The probability score is a model estimate, not a guarantee of fraud.
- Risk thresholds may need adjustment based on validation results and the costs of false positives and false negatives.
- Model performance should be tested on independent, representative data before any real-world deployment.
- Do not upload real card numbers, CVV values, account credentials, or other sensitive financial information to this demonstration application.

## Disclaimer

FraudWatch is intended for educational, portfolio, and demonstration purposes only. It does not provide financial advice, guarantee fraud detection, or replace professional fraud investigation and established payment-security systems.

## Author

**Mrinmoy Choudhury**

GitHub: https://github.com/mrinmoycontent
