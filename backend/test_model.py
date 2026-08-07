import joblib
import pandas as pd
from config import MODEL_PATH, FEATURE_NAMES_PATH

# Load model
model = joblib.load(MODEL_PATH)

# Load feature names
feature_names = joblib.load(FEATURE_NAMES_PATH)

print(f"✅ Model loaded successfully.")
print(f"✅ Number of features: {len(feature_names)}")

# Create one dummy transaction with all features initialized to 0
sample = pd.DataFrame(0, index=[0], columns=feature_names)

# Fill a few sample values
sample["TransactionAmt"] = 1000

# Make prediction
prediction = model.predict(sample)
probability = model.predict_proba(sample)

print("\nPrediction:", prediction[0])
print("Fraud Probability:", probability[0][1])