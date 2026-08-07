from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the trained XGBoost model
MODEL_PATH = BASE_DIR / "models" / "xgboost_fraud_model.pkl"

# Path to the saved feature names
FEATURE_NAMES_PATH = BASE_DIR / "models" / "feature_names.pkl"