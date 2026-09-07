import joblib
import pandas as pd

from backend.config import BASE_DIR

MODEL_PATH = BASE_DIR / "models" / "isolation_forest.pkl"
SCALER_PATH = BASE_DIR / "models" / "anomaly_scaler.pkl"

anomaly_model = joblib.load(MODEL_PATH)
anomaly_scaler = joblib.load(SCALER_PATH)

ANOMALY_FEATURES = [
    "TransactionDT",
    "TransactionAmt",
    "card1",
    "card2",
    "card3",
    "card5",
    "addr1",
    "addr2",
    "dist1",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "C7",
    "C8",
    "C9",
    "C10",
    "C11",
    "C12",
    "C13",
    "C14",
]


def calculate_anomaly(user_input):
    df = pd.DataFrame(
        0.0,
        index=[0],
        columns=ANOMALY_FEATURES
    )

    for feature in ANOMALY_FEATURES:
        if feature in user_input:
            try:
                df.at[0, feature] = float(user_input[feature])
            except (ValueError, TypeError):
                df.at[0, feature] = 0.0

    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.fillna(0)

    X = anomaly_scaler.transform(df)

    prediction = anomaly_model.predict(X)[0]
    raw_score = anomaly_model.decision_function(X)[0]

    is_anomaly = prediction == -1

    anomaly_score = max(
        0,
        min(100, 50 - (raw_score * 100))
    )

    return {
        "is_anomaly": bool(is_anomaly),
        "anomaly_score": round(float(anomaly_score), 2),
        "raw_anomaly_score": round(float(raw_score), 4)
    }