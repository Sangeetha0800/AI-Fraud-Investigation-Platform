import shap
import joblib

from backend.config import MODEL_PATH, FEATURE_NAMES_PATH

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH)

explainer = shap.TreeExplainer(model)


def explain_prediction(features, top_n=10):
    shap_values = explainer(features)

    values = shap_values.values[0]

    explanations = list(zip(feature_names, values))

    explanations.sort(
        key=lambda x: abs(x[1]),
        reverse=True
    )

    top_features = []

    for feature, value in explanations[:top_n]:
        top_features.append({
            "feature": feature,
            "shap_value": float(value),
            "impact": (
                "increases_fraud_risk"
                if value > 0
                else "decreases_fraud_risk"
            )
        })

    return top_features