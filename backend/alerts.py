def generate_alert(fraud_probability, risk_level):

    if risk_level == "Critical":
        alert_level = "CRITICAL"
        alert_generated = True
        reason = "Critical risk level detected. Immediate investigation is required."

    elif risk_level == "High":
        alert_level = "HIGH"
        alert_generated = True
        reason = "High-risk transaction detected. Manual review is recommended."

    elif risk_level == "Medium":
        alert_level = "MEDIUM"
        alert_generated = True
        reason = "Suspicious transaction detected. Additional verification is recommended."

    else:
        alert_level = "LOW"
        alert_generated = False
        reason = "No significant suspicious activity detected."

    return {
        "alert_generated": alert_generated,
        "alert_level": alert_level,
        "reason": reason,
        "fraud_probability": round(float(fraud_probability), 4)
    }