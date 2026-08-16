import joblib
from backend.config import MODEL_PATH
# Load the trained XGBoost model
model = joblib.load(MODEL_PATH)


def predict_transaction(features):
    """
    Predict whether a transaction is Fraud or Legitimate.
    """

    # Make prediction
    prediction = model.predict(features)

    # Get prediction probability
    probability = model.predict_proba(features)

    return {
        "prediction": int(prediction[0]),
        "fraud_probability": float(probability[0][1])
    }