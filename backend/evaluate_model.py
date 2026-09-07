import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from backend.config import BASE_DIR, MODEL_PATH


DATA_PATH = BASE_DIR / "dataset" / "train_transaction.csv"
FEATURE_NAMES_PATH = BASE_DIR / "models" / "feature_names.pkl"

SAMPLE_SIZE = 100000


print("Loading model...")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully.")

print("Loading feature names...")
feature_names = joblib.load(FEATURE_NAMES_PATH)
print(f"Number of model features: {len(feature_names)}")

print(f"Reading {SAMPLE_SIZE} transactions...")

df = pd.read_csv(
    DATA_PATH,
    nrows=SAMPLE_SIZE
)

print("Dataset loaded.")

# Target
y = df["isFraud"]

# Select only the features used by the trained model
X = df.reindex(
    columns=feature_names,
    fill_value=0
)

print("Converting categorical values to numeric values...")

# Convert categorical/string columns to numeric codes
for column in X.columns:

    if X[column].dtype == "object":

        X[column] = X[column].astype("category").cat.codes

# Convert everything to numeric
X = X.apply(pd.to_numeric, errors="coerce")

# Replace missing/infinite values
X = X.replace([float("inf"), float("-inf")], 0)
X = X.fillna(0)

print("Data preparation complete.")
print("Running predictions...")

y_pred = model.predict(X)
y_prob = model.predict_proba(X)[:, 1]


# ==============================
# MODEL METRICS
# ==============================

accuracy = accuracy_score(y, y_pred)

precision = precision_score(
    y,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y,
    y_prob
)

cm = confusion_matrix(
    y,
    y_pred
)


print()
print("==============================")
print("XGBOOST MODEL EVALUATION")
print("==============================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

print()
print("Confusion Matrix:")
print(cm)

print()
print("Classification Report:")
print(
    classification_report(
        y,
        y_pred,
        zero_division=0
    )
)