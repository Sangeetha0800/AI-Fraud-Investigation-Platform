from flask import Flask, request, jsonify

from predict import predict_transaction
from preprocess import preprocess_input
from explain import explain_prediction

app = Flask(__name__)


@app.route("/")
def home():
    return "AI Fraud Investigation Platform Backend is Running Successfully!"


@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Receive JSON data
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No input data provided"
            }), 400

        # Convert investigator input into the 421-feature format
        input_df = preprocess_input(data)

        # Get XGBoost prediction
        result = predict_transaction(input_df)

        # Generate SHAP explanation
        result["shap_explanation"] = explain_prediction(input_df)

        # Return prediction + probability + SHAP explanation
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)