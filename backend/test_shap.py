import pandas as pd
import joblib
import shap

from config import MODEL_PATH, FEATURE_NAMES_PATH

# Load model
model = joblib.load(MODEL_PATH)

# Load feature names
feature_names = joblib.load(FEATURE_NAMES_PATH)

print("✅ Model loaded")
print("✅ Feature names loaded:", len(feature_names))

# Create sample transaction
sample = pd.DataFrame(0, index=[0], columns=feature_names)
sample["TransactionAmt"] = 1000

# Create explainer
explainer = shap.TreeExplainer(model)

print("✅ SHAP Explainer created")

# Calculate SHAP values
shap_values = explainer(sample)

print("Type of SHAP values:", type(shap_values))
print("Shape:", shap_values.values.shape)

print("\nTop 10 SHAP values:")

for feature, value in zip(feature_names[:10], shap_values.values[0][:10]):
    print(feature, ":", value)