import joblib
from backend.config import MODEL_PATH

model = joblib.load(MODEL_PATH)


def predict_transaction(features):
    prediction = model.predict(features)
    probability = model.predict_proba(features)

    return {
        "prediction": int(prediction[0]),
        "fraud_probability": float(probability[0][1])
    }