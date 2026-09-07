def calculate_risk(fraud_probability, anomaly_score):
    fraud_score = fraud_probability * 100

    risk_score = (fraud_score * 0.7) + (anomaly_score * 0.3)

    if risk_score >= 80:
        risk_level = "Critical"
    elif risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level
    }