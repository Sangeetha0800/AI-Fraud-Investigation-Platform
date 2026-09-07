from flask import Flask, request, jsonify

from backend.predict import predict_transaction
from backend.preprocess import preprocess_input
from backend.anomaly import calculate_anomaly
from backend.risk import calculate_risk
from backend.explain import explain_prediction

app = Flask(__name__)


@app.route("/")
def home():
    return "AI Fraud Investigation Platform Backend is Running Successfully!"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No transaction data received"
            }), 400

        # Preprocess input to match the 421 model features
        input_df = preprocess_input(data)

        # XGBoost prediction
        prediction_result = predict_transaction(input_df)

        prediction = prediction_result["prediction"]
        fraud_probability = prediction_result["fraud_probability"]

        # Isolation Forest anomaly detection
        anomaly_result = calculate_anomaly(data)
        anomaly_score = anomaly_result["anomaly_score"]

        # Dynamic risk score
        risk_result = calculate_risk(
            fraud_probability,
            anomaly_score
        )

        # SHAP explanation
        shap_explanation = explain_prediction(
            input_df,
            top_n=10
        )

        # Final response
        result = {
            "prediction": prediction,
            "fraud_probability": round(
                float(fraud_probability), 4
            ),
            "anomaly": anomaly_result,
            "risk": risk_result,
            "shap_explanation": shap_explanation
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    # Debug/reloader disabled because the XGBoost model
    # is large and should not be loaded twice.
    app.run(
        debug=False,
        use_reloader=False,
        host="127.0.0.1",
        port=5000
    )