import pandas as pd
import joblib

from backend.config import FEATURE_NAMES_PATH

feature_names = joblib.load(FEATURE_NAMES_PATH)


def preprocess_input(user_input):
    df = pd.DataFrame(
        0,
        index=[0],
        columns=feature_names
    )

    for key, value in user_input.items():
        if key in df.columns:
            df.at[0, key] = value

    return df