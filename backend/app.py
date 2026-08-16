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
        # 1. Receive transaction data
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No transaction data received"
            }), 400

        # 2. Preprocess input
        input_df = preprocess_input(data)

        # 3. XGBoost fraud prediction
        prediction_result = predict_transaction(input_df)

        prediction = prediction_result["prediction"]
        fraud_probability = prediction_result["fraud_probability"]

        # 4. Anomaly detection
        anomaly_result = calculate_anomaly(data)

        anomaly_score = anomaly_result["anomaly_score"]

        # 5. Dynamic risk scoring
        risk_result = calculate_risk(
            fraud_probability,
            anomaly_score
        )

        # 6. SHAP explanation
        shap_explanation = explain_prediction(
            input_df,
            top_n=10
        )

        # -------------------------------------------------
        # 7. Investigator decision
        # -------------------------------------------------

        risk_level = risk_result["risk_level"]

        if risk_level == "Critical":
            investigation_status = "Immediate investigation required"

        elif risk_level == "High":
            investigation_status = "Manual review recommended"

        elif risk_level == "Medium":
            investigation_status = "Additional verification recommended"

        else:
            investigation_status = "Transaction appears low risk"

        # -------------------------------------------------
        # 8. Final investigation result
        # -------------------------------------------------

        result = {
            "prediction": prediction,

            "fraud_probability": round(
                float(fraud_probability),
                4
            ),

            "anomaly": anomaly_result,

            "risk": risk_result,

            "investigation_status": investigation_status,

            "shap_explanation": shap_explanation
        }

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)