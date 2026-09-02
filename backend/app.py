from flask import Flask, request, jsonify

from backend.predict import predict_transaction
from backend.preprocess import preprocess_input
from backend.anomaly import calculate_anomaly
from backend.risk import calculate_risk
from backend.explain import explain_prediction
from backend.alerts import generate_alert

from backend.cases import (
    initialize_database,
    create_case,
    get_all_cases,
    get_case,
    update_case
)


app = Flask(__name__)


# Initialize Case Management database
initialize_database()


@app.route("/")
def home():
    return "AI Fraud Investigation Platform Backend is Running Successfully!"


# -------------------------------------------------
# PREDICTION + INVESTIGATION PIPELINE
# -------------------------------------------------

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

        # Get risk level
        risk_level = risk_result.get(
            "risk_level",
            "Low"
        )

        # Get risk score safely
        risk_score = risk_result.get(
            "risk_score",
            risk_result.get(
                "score",
                0
            )
        )

        # 6. SHAP explanation
        shap_explanation = explain_prediction(
            input_df,
            top_n=10
        )

        # 7. Investigator decision
        if risk_level == "Critical":

            investigation_status = (
                "Immediate investigation required"
            )

        elif risk_level == "High":

            investigation_status = (
                "Manual review recommended"
            )

        elif risk_level == "Medium":

            investigation_status = (
                "Additional verification recommended"
            )

        else:

            investigation_status = (
                "Transaction appears low risk"
            )

        # 8. Early Warning Alert
        alert_result = generate_alert(
            fraud_probability,
            risk_level
        )

        # -------------------------------------------------
        # 9. Case Management
        # -------------------------------------------------

        case_id = None

        # Create a case only when an alert is generated
        if alert_result["alert_generated"]:

            # Try to find transaction ID
            transaction_id = data.get(
                "TransactionID",
                data.get(
                    "transaction_id",
                    "Unknown"
                )
            )

            case_id = create_case(
                transaction_id=transaction_id,
                fraud_probability=fraud_probability,
                anomaly_score=anomaly_score,
                risk_score=risk_score,
                risk_level=risk_level,
                alert_level=alert_result["alert_level"],
                alert_reason=alert_result["reason"]
            )

        # -------------------------------------------------
        # 10. Final Investigation Result
        # -------------------------------------------------

        result = {

            "prediction": prediction,

            "fraud_probability": round(
                float(fraud_probability),
                4
            ),

            "anomaly": anomaly_result,

            "risk": risk_result,

            "early_warning": alert_result,

            "case_id": case_id,

            "investigation_status": investigation_status,

            "shap_explanation": shap_explanation
        }

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# CASE MANAGEMENT
# -------------------------------------------------

@app.route("/cases", methods=["GET"])
def cases():

    try:

        all_cases = get_all_cases()

        return jsonify({
            "total_cases": len(all_cases),
            "cases": all_cases
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# GET SINGLE CASE
# -------------------------------------------------

@app.route("/cases/<case_id>", methods=["GET"])
def case_details(case_id):

    try:

        case = get_case(case_id)

        if not case:

            return jsonify({
                "error": "Case not found"
            }), 404

        return jsonify(case)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# UPDATE CASE
# -------------------------------------------------

@app.route("/cases/<case_id>", methods=["PUT"])
def modify_case(case_id):

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No case update data received"
            }), 400

        case_status = data.get(
            "case_status"
        )

        investigator_notes = data.get(
            "investigator_notes"
        )

        final_decision = data.get(
            "final_decision"
        )

        updated_case = update_case(
            case_id,
            case_status,
            investigator_notes,
            final_decision
        )

        if not updated_case:

            return jsonify({
                "error": "Case not found"
            }), 404

        return jsonify({
            "message": "Case updated successfully",
            "case": updated_case
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)