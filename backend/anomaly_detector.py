import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "train_transaction.csv"
)

MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "isolation_forest.pkl"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "anomaly_scaler.pkl"
)


# Features selected for behavioral anomaly detection
ANOMALY_FEATURES = [
    "TransactionAmt",
    "TransactionDT",
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
# Train anomaly detector
# ---------------------------------------------------------

def train_anomaly_detector(
    chunksize=10000,
    max_samples=50000
):
    """
    Train Isolation Forest using legitimate transactions.

    The dataset is processed in chunks so that the complete
    683 MB CSV is never loaded into memory.
    """

    print("Starting anomaly detector training...")
    print("Dataset:", DATA_PATH)

    collected = []
    total_legitimate = 0

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            DATA_PATH,
            usecols=["isFraud"] + ANOMALY_FEATURES,
            chunksize=chunksize
        ),
        start=1
    ):

        # Keep legitimate transactions only
        legitimate = chunk[chunk["isFraud"] == 0].drop(
            columns=["isFraud"]
        )

        if len(legitimate) > 0:

            remaining = max_samples - total_legitimate

            if remaining <= 0:
                break

            legitimate = legitimate.iloc[:remaining]

            collected.append(legitimate)
            total_legitimate += len(legitimate)

        print(
            f"Chunk {chunk_number}: "
            f"collected {total_legitimate} legitimate transactions"
        )

        if total_legitimate >= max_samples:
            break

    if not collected:
        raise RuntimeError("No legitimate transactions were collected.")

    # Combine only the selected sample
    data = pd.concat(collected, ignore_index=True)

    print("\nTraining samples:", len(data))
    print("Features:", len(ANOMALY_FEATURES))

    # Convert values to numeric
    data = data.apply(pd.to_numeric, errors="coerce")

    # Replace infinite values
    data = data.replace([float("inf"), float("-inf")], pd.NA)

    # Median imputation
    data = data.fillna(data.median())

    # Scale features
    scaler = StandardScaler()
    X = scaler.fit_transform(data)

    print("Training Isolation Forest...")

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X)

    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save detector
    joblib.dump(model, MODEL_PATH)

    # Save scaler
    joblib.dump(scaler, SCALER_PATH)

    print("\nAnomaly detector trained successfully.")
    print("Model saved to:", MODEL_PATH)
    print("Scaler saved to:", SCALER_PATH)


# ---------------------------------------------------------
# Test anomaly detector
# ---------------------------------------------------------

def test_anomaly_detector():

    print("\nLoading anomaly detector...")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    test_data = pd.read_csv(
        DATA_PATH,
        usecols=ANOMALY_FEATURES,
        nrows=10
    )

    test_data = test_data.apply(
        pd.to_numeric,
        errors="coerce"
    )

    test_data = test_data.replace(
        [float("inf"), float("-inf")],
        pd.NA
    )

    test_data = test_data.fillna(test_data.median())

    X = scaler.transform(test_data)

    predictions = model.predict(X)
    scores = model.decision_function(X)

    print("\nAnomaly test results:")

    for i, (prediction, score) in enumerate(
        zip(predictions, scores)
    ):
        status = (
            "ANOMALY"
            if prediction == -1
            else "NORMAL"
        )

        print(
            f"Transaction {i + 1}: "
            f"{status} | "
            f"Score: {score:.4f}"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    train_anomaly_detector()

    test_anomaly_detector()