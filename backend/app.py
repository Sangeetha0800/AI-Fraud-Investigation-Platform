from flask import Flask, request, jsonify
import pandas as pd

from predict import predict_transaction
from preprocess import preprocess_input

app = Flask(__name__)


@app.route("/")
def home():
    return "AI Fraud Investigation Platform Backend is Running Successfully!"


@app.route("/predict", methods=["POST"])
def predict():

    # Receive JSON data
    data = request.get_json()

    # Convert JSON to DataFrame
    input_df = pd.DataFrame([data])

    # Get prediction
    result = predict_transaction(input_df)

    # Return JSON response
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)