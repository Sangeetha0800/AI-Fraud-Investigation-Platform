import pandas as pd
import joblib
from backend.config import FEATURE_NAMES_PATH# Load feature names once
feature_names = joblib.load(FEATURE_NAMES_PATH)


def preprocess_input(user_input):
    """
    Convert investigator input into the exact feature format
    expected by the trained XGBoost model.
    """

    # Create one-row DataFrame with all 421 features
    df = pd.DataFrame(0, index=[0], columns=feature_names)

    # Fill values provided by the user
    for key, value in user_input.items():
        if key in df.columns:
            df.at[0, key] = value

    return df