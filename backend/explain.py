import shap
import joblib

from backend.config import MODEL_PATH, FEATURE_NAMES_PATH
# Load model and feature names
model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH)

# Create SHAP explainer
explainer = shap.TreeExplainer(model)


def explain_prediction(features, top_n=10):
    """
    Generate SHAP-based explanation for a transaction.
    Returns the top features contributing to the prediction.
    """

    shap_values = explainer(features)

    # Get SHAP values for the first transaction
    values = shap_values.values[0]

    # Pair feature names with their SHAP values
    explanations = list(zip(feature_names, values))

    # Sort by absolute contribution
    explanations.sort(key=lambda x: abs(x[1]), reverse=True)

    # Return top contributing features
    top_features = []

    for feature, value in explanations[:top_n]:
        top_features.append({
            "feature": feature,
            "shap_value": float(value),
            "impact": "increases_fraud_risk" if value > 0 else "decreases_fraud_risk"
        })

    return top_features