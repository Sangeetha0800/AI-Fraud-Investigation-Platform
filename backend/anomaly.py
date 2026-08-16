import joblib
import pandas as pd

from backend.config import BASE_DIR

# ---------------------------------------------------------
# Model paths
# ---------------------------------------------------------

MODEL_PATH = BASE_DIR / "models" / "isolation_forest.pkl"
SCALER_PATH = BASE_DIR / "models" / "anomaly_scaler.pkl"


# ---------------------------------------------------------
# Load anomaly model and scaler once
# ---------------------------------------------------------

anomaly_model = joblib.load(MODEL_PATH)
anomaly_scaler = joblib.load(SCALER_PATH)


# ---------------------------------------------------------
# Features used by the anomaly detector
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# Calculate anomaly
# ---------------------------------------------------------

def calculate_anomaly(user_input):
    """
    Calculate whether a transaction is anomalous.

    Returns:
        is_anomaly
        anomaly_score
        raw_anomaly_score
    """

    # Create one-row dataframe
    df = pd.DataFrame(
        0.0,
        index=[0],
        columns=ANOMALY_FEATURES
    )

    # Fill features supplied by the investigator
    for feature in ANOMALY_FEATURES:

        if feature in user_input:

            try:
                df.at[0, feature] = float(
                    user_input[feature]
                )

            except (ValueError, TypeError):
                df.at[0, feature] = 0.0

    # Make sure everything is numeric
    df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Handle invalid values
    df = df.replace(
        [float("inf"), float("-inf")],
        pd.NA
    )

    df = df.fillna(0)

    # Apply the SAME scaler used during training
    X = anomaly_scaler.transform(df)

    # Isolation Forest prediction
    prediction = anomaly_model.predict(X)[0]

    # Raw decision score
    raw_score = anomaly_model.decision_function(X)[0]

    # -1 = anomaly
    #  1 = normal
    is_anomaly = prediction == -1

    # Convert raw score into a simple 0-100 score.
    # Higher = more anomalous.
    anomaly_score = max(
        0,
        min(
            100,
            50 - (raw_score * 100)
        )
    )

    return {
        "is_anomaly": bool(is_anomaly),
        "anomaly_score": round(
            float(anomaly_score),
            2
        ),
        "raw_anomaly_score": round(
            float(raw_score),
            4
        )
    }