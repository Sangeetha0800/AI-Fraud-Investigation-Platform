def calculate_risk(fraud_probability, anomaly_score):
    """
    Calculate the overall transaction risk.

    fraud_probability: XGBoost probability from 0 to 1
    anomaly_score: Isolation Forest score from 0 to 100
    """

    # Convert fraud probability to percentage
    fraud_score = float(fraud_probability) * 100

    # Keep anomaly score within 0-100
    anomaly_score = max(
        0,
        min(100, float(anomaly_score))
    )

    # Combine both signals
    risk_score = (
        (fraud_score * 0.70) +
        (anomaly_score * 0.30)
    )

    # Keep final score within 0-100
    risk_score = max(
        0,
        min(100, risk_score)
    )

    # Determine risk level
    if risk_score < 25:
        risk_level = "Low"

    elif risk_score < 50:
        risk_level = "Medium"

    elif risk_score < 75:
        risk_level = "High"

    else:
        risk_level = "Critical"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level
    }